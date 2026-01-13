#!/usr/bin/env python3
"""
Track projects in Notion - Universal script for all departments.

Usage:
    python track_project.py --name "Project Name" --department "sales-team" --status "in_progress"
"""

import os
import sys
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path for shared imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from shared.execution.logger import CentralLogger

load_dotenv()

def track_project(project_name, department, status, description="", team_members=None, notion_url=None):
    """
    Create or update a project in Notion.
    
    Args:
        project_name (str): Name of the project
        department (str): Department owning the project
        status (str): Current status (not_started, in_progress, blocked, completed)
        description (str): Project description
        team_members (list): List of team member names
        notion_url (str): Optional - existing Notion page URL to update
        
    Returns:
        dict: Project information with Notion page URL
    """
    logger = CentralLogger(department, "track_project")
    logger.log(f"Tracking project: {project_name} - Status: {status}")
    
    try:
        # Try to use Notion MCP if available
        from notion_client import Client
        
        notion_token = os.getenv('NOTION_API_KEY')
        projects_db_id = os.getenv('NOTION_PROJECTS_DB_ID')
        
        if not notion_token:
            logger.log("NOTION_API_KEY not found, using local fallback", "WARNING")
            return _local_track_project(project_name, department, status, description, team_members)
        
        if not projects_db_id:
            logger.log("NOTION_PROJECTS_DB_ID not set, using local fallback", "WARNING")
            return _local_track_project(project_name, department, status, description, team_members)
        
        notion = Client(auth=notion_token)
        
        # Build properties
        properties = {
            "Name": {
                "title": [{"text": {"content": project_name}}]
            },
            "Status": {
                "select": {"name": status.replace('_', ' ').title()}
            },
            "Department": {
                "select": {"name": department}
            },
            "Last Updated": {
                "date": {"start": datetime.now().isoformat()}
            }
        }
        
        # Add team members if provided
        if team_members:
            properties["Team"] = {
                "multi_select": [{"name": member} for member in team_members]
            }
        
        # Build content blocks
        children = []
        
        if description:
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": description}}]
                }
            })
        
        # Add status tracking section
        children.extend([
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "📊 Progress Tracking"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"text": {"content": f"Current Status: "}},
                        {"text": {"content": status.replace('_', ' ').title()}, "annotations": {"bold": True}}
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "📝 Activity Log"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - Project created/updated by {department}"}}]
                }
            }
        ])
        
        # Check if updating existing page
        if notion_url:
            # Extract page ID from URL
            page_id = notion_url.split('/')[-1].split('?')[0].replace('-', '')
            
            # Update existing page
            page = notion.pages.update(
                page_id=page_id,
                properties=properties
            )
            logger.log(f"Updated existing Notion page: {notion_url}")
        else:
            # Create new page
            page = notion.pages.create(
                parent={"database_id": projects_db_id},
                properties=properties,
                children=children
            )
            logger.log(f"Created new Notion page: {page.get('url')}")
        
        project_info = {
            "project_name": project_name,
            "department": department,
            "status": status,
            "notion_url": page.get('url'),
            "notion_page_id": page.get('id'),
            "last_updated": datetime.now().isoformat()
        }
        
        # Save to .tmp for reference
        os.makedirs('.tmp', exist_ok=True)
        safe_name = project_name.replace(' ', '_').replace('/', '_')
        with open(f'.tmp/project_{safe_name}.json', 'w') as f:
            json.dump(project_info, f, indent=2)
        
        return project_info
        
    except ImportError:
        logger.log("notion_client not installed, using local fallback", "WARNING")
        return _local_track_project(project_name, department, status, description, team_members)
    except Exception as e:
        logger.log(f"Error tracking project in Notion: {e}", "ERROR")
        return _local_track_project(project_name, department, status, description, team_members)

def _local_track_project(project_name, department, status, description, team_members):
    """Fallback: Track project locally when Notion unavailable."""
    logger = CentralLogger(department, "track_project_local")
    
    project_info = {
        "project_name": project_name,
        "department": department,
        "status": status,
        "description": description,
        "team_members": team_members or [],
        "notion_url": None,
        "last_updated": datetime.now().isoformat(),
        "mode": "local_fallback"
    }
    
    os.makedirs('.tmp', exist_ok=True)
    safe_name = project_name.replace(' ', '_').replace('/', '_')
    filepath = f'.tmp/project_{safe_name}.json'
    
    with open(filepath, 'w') as f:
        json.dump(project_info, f, indent=2)
    
    logger.log(f"Project tracked locally: {filepath}")
    return project_info

def main():
    parser = argparse.ArgumentParser(description='Track project in Notion')
    parser.add_argument('--name', required=True, help='Project name')
    parser.add_argument('--department', required=True, help='Department name')
    parser.add_argument('--status', required=True, choices=['not_started', 'in_progress', 'blocked', 'completed'])
    parser.add_argument('--description', default='', help='Project description')
    parser.add_argument('--team', nargs='+', help='Team member names')
    parser.add_argument('--url', help='Existing Notion page URL to update')
    
    args = parser.parse_args()
    
    result = track_project(
        project_name=args.name,
        department=args.department,
        status=args.status,
        description=args.description,
        team_members=args.team,
        notion_url=args.url
    )
    
    print("\n=== Project Tracked ===")
    print(json.dumps(result, indent=2))
    
    if result.get('notion_url'):
        print(f"\n✅ View in Notion: {result['notion_url']}")
    else:
        print(f"\n📁 Tracked locally (Notion unavailable)")

if __name__ == "__main__":
    main()
