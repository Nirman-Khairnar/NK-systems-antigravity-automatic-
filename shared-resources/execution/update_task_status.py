#!/usr/bin/env python3
"""
Update task status in Notion - Real-time updates for active work.

Usage:
    python update_task_status.py --task "Task Name" --status "in_progress" --notes "Updated the API integration"
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

def update_task_status(task_identifier, new_status, progress_notes="", department=""):
    """
    Update task status in Notion with real-time progress.
    
    Args:
        task_identifier (str): Task name or Notion page ID/URL
        new_status (str): New status value
        progress_notes (str): What changed/progress made
        department (str): Department making the update
        
    Returns:
        dict: Updated task information
    """
    logger = CentralLogger(department or "system", "update_task_status")
    logger.log(f"Updating task: {task_identifier} -> {new_status}")
    
    try:
        from notion_client import Client
        
        notion_token = os.getenv('NOTION_API_KEY')
        if not notion_token:
            logger.log("NOTION_API_KEY not found, using local fallback", "WARNING")
            return _local_update_task(task_identifier, new_status, progress_notes, department)
        
        notion = Client(auth=notion_token)
        
        # Determine if it's a page ID or need to search
        page_id = None
        if len(task_identifier) == 32 or 'notion.so' in task_identifier:
            # It's a Notion URL or ID
            page_id = task_identifier.split('/')[-1].split('?')[0].replace('-', '')
        else:
            # Search for task by name
            tasks_db_id = os.getenv('NOTION_TASKS_DB_ID')
            if tasks_db_id:
                search_results = notion.databases.query(
                    database_id=tasks_db_id,
                    filter={
                        "property": "Name",
                        "title": {
                            "contains": task_identifier
                        }
                    }
                )
                if search_results.get('results'):
                    page_id = search_results['results'][0]['id']
        
        if not page_id:
            logger.log(f"Could not find task: {task_identifier}", "WARNING")
            return _local_update_task(task_identifier, new_status, progress_notes, department)
        
        # Update status property
        properties = {
            "Status": {
                "select": {"name": new_status.replace('_', ' ').title()}
            },
            "Last Updated": {
                "date": {"start": datetime.now().isoformat()}
            }
        }
        
        if department:
            properties["Updated By"] = {
                "rich_text": [{"text": {"content": department}}]
            }
        
        page = notion.pages.update(page_id=page_id, properties=properties)
        
        # Append progress notes to page
        if progress_notes:
            notion.blocks.children.append(
                block_id=page_id,
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {"text": {"content": f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] "}},
                                {"text": {"content": progress_notes}}
                            ]
                        }
                    }
                ]
            )
        
        logger.log(f"Task updated successfully: {page.get('url')}")
        
        return {
            "task_identifier": task_identifier,
            "new_status": new_status,
            "notes": progress_notes,
            "notion_url": page.get('url'),
            "updated_at": datetime.now().isoformat()
        }
        
    except ImportError:
        logger.log("notion_client not installed, using local fallback", "WARNING")
        return _local_update_task(task_identifier, new_status, progress_notes, department)
    except Exception as e:
        logger.log(f"Error updating task: {e}", "ERROR")
        return _local_update_task(task_identifier, new_status, progress_notes, department)

def _local_update_task(task_identifier, new_status, progress_notes, department):
    """Fallback: Update task locally."""
    logger = CentralLogger(department or "system", "update_task_local")
    
    update_record = {
        "task_identifier": task_identifier,
        "new_status": new_status,
        "progress_notes": progress_notes,
        "department": department,
        "updated_at": datetime.now().isoformat(),
        "mode": "local_fallback"
    }
    
    os.makedirs('.tmp', exist_ok=True)
    filepath = f'.tmp/task_updates.jsonl'
    
    with open(filepath, 'a') as f:
        f.write(json.dumps(update_record) + '\n')
    
    logger.log(f"Task update logged locally: {filepath}")
    return update_record

def main():
    parser = argparse.ArgumentParser(description='Update task status in Notion')
    parser.add_argument('--task', required=True, help='Task name or Notion page ID/URL')
    parser.add_argument('--status', required=True, help='New status')
    parser.add_argument('--notes', default='', help='Progress notes')
    parser.add_argument('--department', default='', help='Department making the update')
    
    args = parser.parse_args()
    
    result = update_task_status(
        task_identifier=args.task,
        new_status=args.status,
        progress_notes=args.notes,
        department=args.department
    )
    
    print("\n=== Task Updated ===")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
