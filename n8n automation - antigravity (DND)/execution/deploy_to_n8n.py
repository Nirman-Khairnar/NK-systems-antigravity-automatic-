#!/usr/bin/env python3
"""
Deploy n8n workflow programmatically via API.
"""

import os
import json
import logging
from dotenv import load_dotenv
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def deploy_to_n8n(workflow_path, environment="staging", output_dir=".tmp"):
    """
    Deploy workflow to n8n instance.
    
    Args:
        workflow_path (str): Path to workflow.json
        environment (str): 'staging' or 'production'
        output_dir (str): Directory to save deployment info
        
    Returns:
        dict: Deployment information
    """
    logger.info(f"Deploying workflow from {workflow_path} to {environment}")
    
    # Get n8n credentials
    api_url = os.getenv('N8N_API_URL')
    api_key = os.getenv('N8N_API_KEY')
    
    if not api_url or not api_key:
        raise ValueError("N8N_API_URL and N8N_API_KEY must be set in .env")
    
    # Remove trailing slash from URL
    api_url = api_url.rstrip('/')
    
    # Load workflow
    with open(workflow_path, 'r') as f:
        workflow_data = json.load(f)
    # Remove 'active' field if present (read-only in API)
    if 'active' in workflow_data:
        del workflow_data['active']
        
    # Remove 'tags' field if present (read-only in API)
    if 'tags' in workflow_data:
        del workflow_data['tags']
    
    # Sanitize nodes - remove extra properties that cause API errors
    valid_node_keys = [
        'id', 'name', 'type', 'typeVersion', 'position', 
        'parameters', 'credentials', 'disabled', 'notes',
        'continueOnFail', 'retryOnFail'
    ]
    
    if 'nodes' in workflow_data:
        for node in workflow_data['nodes']:
            # Remove keys not in allowlist
            keys_to_remove = [k for k in node.keys() if k not in valid_node_keys]
            for k in keys_to_remove:
                logger.info(f"Removing invalid key '{k}' from node '{node.get('name')}'")
                del node[k]

    # Valid keys sanitization is done above
    
    # Send request
    logger.info("Creating new workflow")
    # Tags removed to prevent read-only error
    if 'tags' in workflow_data:
        del workflow_data['tags']
    
    # Prepare headers
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        # Create or update workflow
        # First, try to find existing workflow by name
        logger.info("Checking for existing workflow")
        list_url = f"{api_url}/api/v1/workflows"
        
        response = requests.get(list_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        existing_workflows = response.json().get('data', [])
        existing = None
        for wf in existing_workflows:
            if wf.get('name') == workflow_data.get('name'):
                existing = wf
                break

        if existing:
            # Update existing workflow
            workflow_id = existing['id']
            logger.info(f"Updating existing workflow: {workflow_id}")
            update_url = f"{api_url}/api/v1/workflows/{workflow_id}"
            
            response = requests.put(update_url, headers=headers, json=workflow_data, timeout=30)
            response.raise_for_status()
            result = response.json()
        else:
            # Create new workflow
            logger.info("Creating new workflow")
            create_url = f"{api_url}/api/v1/workflows"
            
            response = requests.post(create_url, headers=headers, json=workflow_data, timeout=30)
            response.raise_for_status()
            result = response.json()
        
        workflow_id = result.get('id')
        
        # Activate workflow if staging
        if environment == "staging":
            logger.info(f"Activating workflow {workflow_id}")
            activate_url = f"{api_url}/api/v1/workflows/{workflow_id}/activate"
            requests.post(activate_url, headers=headers, timeout=30)
        
        # Save deployment info
        deployment_info = {
            "workflow_id": workflow_id,
            "workflow_name": workflow_data.get('name'),
            "environment": environment,
            "n8n_url": api_url,
            "status": "active" if environment == "staging" else "inactive",
            "tags": workflow_data.get('tags', [])
        }
        
        os.makedirs(output_dir, exist_ok=True)
        info_path = os.path.join(output_dir, "deployment_info.json")
        with open(info_path, 'w') as f:
            json.dump(deployment_info, f, indent=2)
        
        logger.info(f"Deployment successful! Workflow ID: {workflow_id}")
        return deployment_info
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to deploy workflow: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response: {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        raise

def main():
    """Main execution for testing."""
    import sys
    
    workflow_path = ".tmp/workflow.json" if len(sys.argv) < 2 else sys.argv[1]
    environment = "staging" if len(sys.argv) < 3 else sys.argv[2]
    
    if not os.path.exists(workflow_path):
        print(f"Error: {workflow_path} not found")
        print("Run generate_workflow.py first")
        sys.exit(1)
    
    deployment_info = deploy_to_n8n(workflow_path, environment)
    
    print("\n=== Deployment Successful ===")
    print(json.dumps(deployment_info, indent=2))

if __name__ == "__main__":
    main()
