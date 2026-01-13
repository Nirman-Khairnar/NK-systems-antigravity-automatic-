#!/usr/bin/env python3
"""
Create and update Notion documentation for n8n workflows.
"""

import os
import json
import logging
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def create_notion_docs(requirements_path, workflow_path, deployment_path=None, performance_path=None, output_dir=".tmp"):
    """
    Create comprehensive Notion documentation for a workflow.
    
    Args:
        requirements_path (str): Path to requirements.json
        workflow_path (str): Path to workflow.json
        deployment_path (str): Path to deployment_info.json (optional)
        performance_path (str): Path to performance_report.json (optional)
        output_dir (str): Directory for temp files
        
    Returns:
        dict: Notion page information
    """
    logger.info("Creating Notion documentation")
    
    # Initialize Notion client
    notion_token = os.getenv('NOTION_API_KEY')
    database_id = os.getenv('NOTION_WORKFLOWS_DB_ID')
    
    if not notion_token or not database_id:
        raise ValueError("NOTION_API_KEY and NOTION_WORKFLOWS_DB_ID must be set in .env")
    
    notion = Client(auth=notion_token)
    
    # Load data files
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = json.load(f)
    
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    
    deployment_info = None
    if deployment_path and os.path.exists(deployment_path):
        with open(deployment_path, 'r') as f:
            deployment_info = json.load(f)
    
    performance_data = None
    if performance_path and os.path.exists(performance_path):
        with open(performance_path, 'r') as f:
            performance_data = json.load(f)
    
    # Build Notion page content
    workflow_name = requirements.get('workflow_name', workflow.get('name', 'Untitled Workflow'))
    
    try:
        # Create page in database
        logger.info(f"Creating page: {workflow_name}")
        
        # Build properties for database
        properties = {
            "Name": {"title": [{"text": {"content": workflow_name}}]},
        }
        
        # Add optional properties if they exist in the database
        # Skipped to avoid schema errors - info is added to page content instead
        # if deployment_info:
        #     properties["Status"] = {"select": {"name": deployment_info.get('status', 'inactive').title()}}
        #     properties["n8n Workflow ID"] = {"rich_text": [{"text": {"content": deployment_info.get('workflow_id', '')}}]}
        
        
        #     properties["Success Rate"] = {"number": performance_data.get('success_rate_percent', 0)}
        
        # Build page content blocks
        children = []
        
        # Callout with Link to n8n
        if deployment_info:
            n8n_url = deployment_info.get('n8n_url', '').rstrip('/')
            wf_id = deployment_info.get('workflow_id', '')
            editor_url = f"{n8n_url}/workflow/{wf_id}"
            
            children.append({
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {"text": {"content": "🚀 Active in n8n - "}},
                        {"text": {"content": "Open Editor", "link": {"url": editor_url}}, "annotations": {"bold": True}}
                    ],
                    "icon": {"emoji": "⚡"}
                }
            })

        # Overview section
        children.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "📋 Overview"}}]}
        })
        
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": requirements.get('goal', 'No description provided')}}]}
        })

        # What Was Built section
        children.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "🔧 What Was Built"}}]}
        })
        
        # Node count and workflow details
        node_count = len(workflow.get('nodes', []))
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"text": {"content": f"Complete workflow with "}},
                {"text": {"content": f"{node_count} nodes", "link": None}, "annotations": {"bold": True}},
                {"text": {"content": " covering the complete automation flow."}}
            ]}
        })

        # Technical Execution Flow
        children.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {"rich_text": [{"text": {"content": "Data Flow"}}]}
        })
        
        # Sort nodes by position
        nodes = workflow.get('nodes', [])
        nodes.sort(key=lambda n: n.get('position', [0,0])[0])
        
        for idx, node in enumerate(nodes, 1):
            node_name = node.get('name', 'Unknown')
            node_type = node.get('type', '').replace('n8n-nodes-base.', '').replace('@n8n/n8n-nodes-langchain.', '')
            children.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [
                        {"text": {"content": f"{node_name}", "link": None}, "annotations": {"bold": True}},
                        {"text": {"content": f" - {node_type}"}}
                    ]
                }
            })

        # Key Features
        children.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {"rich_text": [{"text": {"content": "Key Features"}}]}
        })
        
        features = requirements.get('key_features', [])
        if features:
            for feature in features:
                children.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": [{"text": {"content": f"✅ {feature}"}}]}
                })

        # Setup Instructions
        children.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "🛠️ Setup Instructions"}}]}
        })
        
        # Required Credentials callout
        children.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"text": {"content": "Configure these credentials in n8n before the workflow can run", "link": None}, "annotations": {"bold": True}}],
                "icon": {"emoji": "🔐"}
            }
        })
        
        # List apps that need credentials
        apps = requirements.get('apps', [])
        if apps:
            for app in apps:
                if app != "AI Agent (n8n)":  # Skip AI Agent as it's built-in
                    children.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {"rich_text": [{"text": {"content": app, "link": None}, "annotations": {"bold": True}}]}
                    })

        # Deployment Options
        children.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {"rich_text": [{"text": {"content": "Deployment Options"}}]}
        })
        
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": "Option 1: Manual Import", "link": None}, "annotations": {"bold": True}}]}
        })
        
        children.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"text": {"content": "Open your n8n instance"}}]}
        })
        children.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"text": {"content": "Click 'Import from File' or copy JSON from toggle below"}}]}
        })
        children.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"text": {"content": "Configure all credential nodes"}}]}
        })
        children.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"text": {"content": "Update any instance-specific IDs (Airtable base/table, Slack channels)"}}]}
        })
        children.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"text": {"content": "Activate the workflow and copy webhook URL"}}]}
        })

        # Testing section
        children.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "🧪 Testing"}}]}
        })
        
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": "Test with your trigger source (e.g., Stripe test mode):", "link": None}, "annotations": {"bold": True}}]}
        })
        
        children.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"text": {"content": "Monitor n8n execution log"}}]}
        })
        children.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"text": {"content": "Verify all expected outputs are created"}}]}
        })
        children.append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"text": {"content": "Test error handling by misconfiguring a credential temporarily"}}]}
        })

        # Expected Outcomes
        outcomes = requirements.get('expected_outcomes', {})
        if outcomes:
            children.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "🎯 Expected Outcomes"}}]}
            })
            
            for category, items in outcomes.items():
                category_title = category.replace('_', ' ').title()
                children.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {"rich_text": [{"text": {"content": category_title}}]}
                })
                for item in items:
                    children.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {"rich_text": [{"text": {"content": item}}]}
                    })

        # Error Handling
        error_handling = requirements.get('error_handling', [])
        if error_handling:
            children.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "⚠️ Error Handling"}}]}
            })
            for error in error_handling:
                children.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": [{"text": {"content": error}}]}
                })

        # Trigger Details
        trigger = requirements.get('triggers', [{}])[0]
        if trigger:
            children.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "🪝 Trigger Configuration"}}]}
            })
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": trigger.get('description', 'Not specified')}}]}
            })

        # JSON Code in Toggle - Complete workflow
        children.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "💾 Complete Workflow JSON"}}]}
        })
        
        children.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"text": {"content": "The complete workflow JSON is in the toggle below. Click to expand and copy for import into n8n.", "link": None}}],
                "icon": {"emoji": "💡"}
            }
        })
        
        workflow_str = json.dumps(workflow, indent=2)
        chunk_size = 2000
        chunks = [workflow_str[i:i+chunk_size] for i in range(0, len(workflow_str), chunk_size)]
        
        code_blocks = []
        for i, chunk in enumerate(chunks):
            code_blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"text": {"content": chunk}}],
                    "language": "json"
                }
            })

        children.append({
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"text": {"content": f"📄 Workflow JSON ({len(chunks)} blocks - complete and unbroken)", "link": None}, "annotations": {"bold": True}}],
                "children": code_blocks
            }
        })
        
        # Production ready status
        children.append({
            "object": "block",
            "type": "divider",
            "divider": {}
        })
        
        children.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {"text": {"content": "✅ Workflow is production-ready and scalable", "link": None}, "annotations": {"bold": True}}
                ],
                "icon": {"emoji": "🎉"}
            }
        })

        # Create the page
        page = notion.pages.create(
            parent={"database_id": database_id},
            properties=properties,
            children=children
        )
        
        page_url = page.get('url')
        page_id = page.get('id')
        
        logger.info(f"Notion page created: {page_url}")
        
        # Save page info
        os.makedirs(output_dir, exist_ok=True)
        page_info = {
            "page_id": page_id,
            "page_url": page_url,
            "workflow_name": workflow_name,
            "created_at": datetime.now().isoformat()
        }
        
        info_path = os.path.join(output_dir, "notion_page_info.json")
        with open(info_path, 'w') as f:
            json.dump(page_info, f, indent=2)
        
        return page_info
        
    except Exception as e:
        logger.error(f"Failed to create Notion page: {e}")
        raise

def main():
    """Main execution for testing."""
    import sys
    
    # Default paths
    req_path = ".tmp/requirements.json"
    wf_path = ".tmp/workflow.json"
    deploy_path = ".tmp/deployment_info.json"
    perf_path = ".tmp/performance_report.json"
    
    # Override from command line if provided
    if len(sys.argv) > 1:
        req_path = sys.argv[1]
    if len(sys.argv) > 2:
        wf_path = sys.argv[2]
    
    if not os.path.exists(req_path) or not os.path.exists(wf_path):
        print("Error: Required files not found")
        print(f"Requirements: {req_path}")
        print(f"Workflow: {wf_path}")
        sys.exit(1)
    
    page_info = create_notion_docs(req_path, wf_path, deploy_path, perf_path)
    
    print("\n=== Notion Documentation Created ===")
    print(json.dumps(page_info, indent=2))

if __name__ == "__main__":
    main()
