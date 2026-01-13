#!/usr/bin/env python3
"""
Log changes to projects/tasks in Notion - Track all modifications.

Usage:
    python log_change.py --project "Project Name" --change "Updated requirements" --department "sales-team"
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

def log_change(project_name, change_description, department, change_type="update", impact="low"):
    """
    Log a change to a project in Notion.
    
    Args:
        project_name (str): Name of the project
        change_description (str): What changed
        department (str): Department making the change
        change_type (str): Type of change (requirement, approach, blocker, completion)
        impact (str): Impact level (low, medium, high, critical)
        
    Returns:
        dict: Change log entry
    """
    logger = CentralLogger(department, "log_change")
    logger.log(f"Logging change for {project_name}: {change_description}")
    
    change_entry = {
        "project_name": project_name,
        "change_description": change_description,
        "department": department,
        "change_type": change_type,
        "impact": impact,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        from notion_client import Client
        
        notion_token = os.getenv('NOTION_API_KEY')
        if not notion_token:
            return _local_log_change(change_entry)
        
        notion = Client(auth=notion_token)
        
        # Find project page
        projects_db_id = os.getenv('NOTION_PROJECTS_DB_ID')
        if not projects_db_id:
            return _local_log_change(change_entry)
        
        search_results = notion.databases.query(
            database_id=projects_db_id,
            filter={
                "property": "Name",
                "title": {
                    "contains": project_name
                }
            }
        )
        
        if not search_results.get('results'):
            logger.log(f"Project not found: {project_name}", "WARNING")
            return _local_log_change(change_entry)
        
        page_id = search_results['results'][0]['id']
        
        # Add change log entry to page
        emoji_map = {
            "requirement": "📝",
            "approach": "🔄",
            "blocker": "🚫",
            "completion": "✅",
            "update": "📌"
        }
        
        impact_emoji = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴"
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
                            {"text": {"content": f"{change_description}", "link": None}, "annotations": {"bold": True}},
                            {"text": {"content": f" - {department}"}}
                        ],
                        "icon": {"emoji": emoji_map.get(change_type, "📌")},
                        "color": "gray_background" if impact == "low" else "yellow_background" if impact == "medium" else "orange_background"
                    }
                }
            ]
        )
        
        logger.log(f"Change logged in Notion for project: {project_name}")
        change_entry["notion_logged"] = True
        
        return change_entry
        
    except ImportError:
        return _local_log_change(change_entry)
    except Exception as e:
        logger.log(f"Error logging change: {e}", "ERROR")
        return _local_log_change(change_entry)

def _local_log_change(change_entry):
    """Fallback: Log change locally."""
    logger = CentralLogger(change_entry['department'], "log_change_local")
    
    os.makedirs('.tmp', exist_ok=True)
    filepath = f'.tmp/change_log.jsonl'
    
    change_entry["notion_logged"] = False
    change_entry["mode"] = "local_fallback"
    
    with open(filepath, 'a') as f:
        f.write(json.dumps(change_entry) + '\n')
    
    logger.log(f"Change logged locally: {filepath}")
    return change_entry

def main():
    parser = argparse.ArgumentParser(description='Log change to project in Notion')
    parser.add_argument('--project', required=True, help='Project name')
    parser.add_argument('--change', required=True, help='Change description')
    parser.add_argument('--department', required=True, help='Department making change')
    parser.add_argument('--type', default='update', choices=['requirement', 'approach', 'blocker', 'completion', 'update'])
    parser.add_argument('--impact', default='low', choices=['low', 'medium', 'high', 'critical'])
    
    args = parser.parse_args()
    
    result = log_change(
        project_name=args.project,
        change_description=args.change,
        department=args.department,
        change_type=args.type,
        impact=args.impact
    )
    
    print("\n=== Change Logged ===")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
