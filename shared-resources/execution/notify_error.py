#!/usr/bin/env python3
"""
Notify user of technical errors immediately - Fast escalation.

Usage:
    python notify_error.py --type "api_limit" --service "Scraper API" --details "Limit reached" --impact "blocking"
"""

import os
import sys
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from shared_resources.execution.logger import CentralLogger

load_dotenv()

def notify_error(error_type, service, details, impact="blocking", options=None, project=""):
    """
    Immediately notify user of technical error.
    
    Args:
        error_type (str): Type of error (api_limit, integration_missing, auth_failure, system_error)
        service (str): Which service/tool has the error
        details (str): Specific error details
        impact (str): Impact level (blocking, warning, info)
        options (list): Possible resolution options
        project (str): Which project is affected
        
    Returns:
        dict: Error notification record
    """
    logger = CentralLogger("engineering-team", "notify_error")
    
    error_id = f"err-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    error_record = {
        "error_id": error_id,
        "error_type": error_type,
        "service": service,
        "details": details,
        "impact": impact,
        "options": options or [],
        "project": project,
        "timestamp": datetime.now().isoformat(),
        "status": "escalated"
    }
    
    # Log to central log
    logger.log(f"ERROR ESCALATED: {error_type} in {service} - {details} [Impact: {impact}]", "ERROR")
    
    # Save error record
    os.makedirs('.tmp', exist_ok=True)
    with open(f'.tmp/error_{error_id}.json', 'w') as f:
        json.dump(error_record, f, indent=2)
    
    # Append to error log
    with open('.tmp/errors.jsonl', 'a') as f:
        f.write(json.dumps(error_record) + '\n')
    
    # Try to notify via Notion
    try:
        from notion_client import Client
        
        notion_token = os.getenv('NOTION_API_KEY')
        projects_db_id = os.getenv('NOTION_PROJECTS_DB_ID')
        
        if notion_token and projects_db_id and project:
            notion = Client(auth=notion_token)
            
            # Find project page
            search_results = notion.databases.query(
                database_id=projects_db_id,
                filter={
                    "property": "Name",
                    "title": {"contains": project}
                }
            )
            
            if search_results.get('results'):
                page_id = search_results['results'][0]['id']
                
                # Add error alert to page
                emoji_map = {
                    "blocking": "🔴",
                    "warning": "🟡",
                    "info": "🔵"
                }
                
                notion.blocks.children.append(
                    block_id=page_id,
                    children=[
                        {
                            "object": "block",
                            "type": "callout",
                            "callout": {
                                "rich_text": [
                                    {"text": {"content": f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] "}},
                                    {"text": {"content": f"ERROR: {error_type.upper()}", "link": None}, "annotations": {"bold": True}},
                                    {"text": {"content": f" - {service}\n{details}"}}
                                ],
                                "icon": {"emoji": emoji_map.get(impact, "🔴")},
                                "color": "red_background" if impact == "blocking" else "yellow_background"
                            }
                        }
                    ]
                )
                
                logger.log(f"Error logged to Notion project: {project}")
    except Exception as e:
        logger.log(f"Could not log to Notion: {e}", "WARNING")
    
    # Print user-facing notification
    print(f"\n{'='*60}")
    print(f"⚠️  TECHNICAL ERROR - USER ATTENTION REQUIRED")
    print(f"{'='*60}\n")
    print(f"Error Type: {error_type.upper().replace('_', ' ')}")
    print(f"Service: {service}")
    print(f"Impact: {impact.upper()}")
    if project:
        print(f"Affected Project: {project}")
    print(f"\nDetails:\n{details}\n")
    
    if options:
        print(f"Resolution Options:")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        print()
    
    print(f"Error ID: {error_id}")
    print(f"Logged: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # This error should trigger AI Orchestrator to use notify_user
    # For now, create a flag file that orchestrator can check
    with open('.tmp/ESCALATION_NEEDED.flag', 'w') as f:
        f.write(error_id)
    
    return error_record

def main():
    parser = argparse.ArgumentParser(description='Notify user of technical error')
    parser.add_argument('--type', required=True, choices=['api_limit', 'integration_missing', 'auth_failure', 'system_error'])
    parser.add_argument('--service', required=True, help='Service/tool with error')
    parser.add_argument('--details', required=True, help='Error details')
    parser.add_argument('--impact', default='blocking', choices=['blocking', 'warning', 'info'])
    parser.add_argument('--options', nargs='+', help='Resolution options')
    parser.add_argument('--project', default='', help='Affected project name')
    
    args = parser.parse_args()
    
    result = notify_error(
        error_type=args.type,
        service=args.service,
        details=args.details,
        impact=args.impact,
        options=args.options,
        project=args.project
    )
    
    print(f"✅ Error notification created: {result['error_id']}")
    print(f"📁 Logged to: .tmp/error_{result['error_id']}.json")

if __name__ == "__main__":
    main()
