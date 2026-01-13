"""
Deploy n8n Workflow
Uploads workflow JSON to n8n instance via API
"""

import os
import json
import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_workflow(workflow_file):
    """Load and validate workflow JSON"""
    try:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
        
        # Validate required fields
        if 'name' not in workflow:
            raise ValueError("Workflow must have a 'name' field")
        if 'nodes' not in workflow:
            raise ValueError("Workflow must have a 'nodes' field")
        if 'connections' not in workflow:
            raise ValueError("Workflow must have a 'connections' field")
        
        print(f"✓ Loaded workflow: {workflow['name']}")
        print(f"  - Nodes: {len(workflow['nodes'])}")
        print(f"  - Connections: {len(workflow['connections'])}")
        
        return workflow
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in workflow file: {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Workflow file not found: {workflow_file}")

def check_existing_workflow(n8n_url, api_key, workflow_name):
    """Check if workflow with this name already exists"""
    headers = {
        'X-N8N-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f"{n8n_url}/api/v1/workflows", headers=headers)
        response.raise_for_status()
        
        workflows = response.json()
        for wf in workflows.get('data', []):
            if wf.get('name') == workflow_name:
                return wf.get('id')
        
        return None
    except requests.exceptions.RequestException:
        # If we can't check, assume it doesn't exist
        return None

def deploy_workflow(workflow_file, update_existing=True):
    """Deploy workflow to n8n instance"""
    
    # Get configuration from environment
    n8n_url = os.getenv('N8N_URL')
    api_key = os.getenv('N8N_API_KEY')
    
    if not n8n_url:
        raise ValueError("N8N_URL not found in environment variables")
    if not api_key:
        raise ValueError("N8N_API_KEY not found in environment variables")
    
    # Remove trailing slash from URL
    n8n_url = n8n_url.rstrip('/')
    
    print(f"\n📡 Connecting to n8n instance: {n8n_url}")
    
    # Load workflow
    workflow = load_workflow(workflow_file)
    workflow_name = workflow['name']
    
    # Check if workflow exists
    existing_id = check_existing_workflow(n8n_url, api_key, workflow_name)
    
    headers = {
        'X-N8N-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        if existing_id and update_existing:
            # Update existing workflow
            print(f"\n🔄 Updating existing workflow (ID: {existing_id})...")
            url = f"{n8n_url}/api/v1/workflows/{existing_id}"
            response = requests.put(url, headers=headers, json=workflow)
        else:
            # Create new workflow
            print(f"\n✨ Creating new workflow...")
            url = f"{n8n_url}/api/v1/workflows"
            response = requests.post(url, headers=headers, json=workflow)
        
        response.raise_for_status()
        result = response.json()
        
        workflow_id = result.get('id')
        print(f"\n✅ Workflow deployed successfully!")
        print(f"   Workflow ID: {workflow_id}")
        print(f"   Name: {workflow_name}")
        
        # Extract webhook URLs if present
        webhook_urls = []
        for node in workflow.get('nodes', []):
            if node.get('type') == 'n8n-nodes-base.webhook':
                webhook_path = node.get('parameters', {}).get('path', '')
                if webhook_path:
                    webhook_url = f"{n8n_url}/webhook/{webhook_path}"
                    webhook_urls.append({
                        'node': node.get('name'),
                        'url': webhook_url
                    })
        
        if webhook_urls:
            print(f"\n🪝 Webhook URLs:")
            for webhook in webhook_urls:
                print(f"   {webhook['node']}: {webhook['url']}")
            print(f"\n💡 Configure these webhook URLs in your external services (e.g., Stripe)")
        
        return {
            'success': True,
            'workflow_id': workflow_id,
            'workflow_name': workflow_name,
            'webhook_urls': webhook_urls
        }
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Deployment failed: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        return {
            'success': False,
            'error': str(e)
        }

def main():
    parser = argparse.ArgumentParser(description='Deploy n8n workflow')
    parser.add_argument('--workflow-file', required=True, help='Path to workflow JSON file')
    parser.add_argument('--no-update', action='store_true', help='Do not update existing workflow')
    
    args = parser.parse_args()
    
    try:
        result = deploy_workflow(args.workflow_file, update_existing=not args.no_update)
        
        if result['success']:
            print(f"\n🎉 Deployment complete!")
            return 0
        else:
            print(f"\n⚠️ Deployment failed")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
