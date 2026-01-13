#!/usr/bin/env python3
"""
Log improvements after operations - Continuous improvement tracking.

Usage:
    python log_improvement.py --department "engineering-team" --operation "Built workflow" --improvement "Created templates" --impact "30% faster"
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

def log_improvement(department, operation, improvement, impact, category="efficiency"):
    """
    Log an improvement made after completing an operation.
    
    Args:
        department (str): Department that made the improvement
        operation (str): What operation was improved
        improvement (str): What improvement was made
        impact (str): Measurable impact of improvement
        category (str): Type of improvement (efficiency, automation, quality, etc.)
        
    Returns:
        dict: Improvement record
    """
    logger = CentralLogger(department, "log_improvement")
    
    improvement_record = {
        "department": department,
        "operation": operation,
        "improvement": improvement,
        "impact": impact,
        "category": category,
        "timestamp": datetime.now().isoformat()
    }
    
    # Log to central log
    logger.log(f"IMPROVEMENT: {department} improved '{operation}' - {improvement} (Impact: {impact})")
    
    # Save to improvements log
    os.makedirs('.tmp', exist_ok=True)
    filepath = '.tmp/improvements.jsonl'
    
    with open(filepath, 'a') as f:
        f.write(json.dumps(improvement_record) + '\n')
    
    # Try to log to Notion if available
    try:
        from notion_client import Client
        
        notion_token = os.getenv('NOTION_API_KEY')
        improvements_db_id = os.getenv('NOTION_IMPROVEMENTS_DB_ID')
        
        if notion_token and improvements_db_id:
            notion = Client(auth=notion_token)
            
            # Create improvement entry in Notion
            notion.pages.create(
                parent={"database_id": improvements_db_id},
                properties={
                    "Name": {
                        "title": [{"text": {"content": f"{operation} - {improvement[:100]}"}}]
                    },
                    "Department": {
                        "select": {"name": department}
                    },
                    "Category": {
                        "select": {"name": category}
                    },
                    "Impact": {
                        "rich_text": [{"text": {"content": impact}}]
                    },
                    "Date": {
                        "date": {"start": datetime.now().isoformat()}
                    }
                }
            )
            
            improvement_record["notion_logged"] = True
            logger.log("Improvement logged to Notion")
    except Exception as e:
        logger.log(f"Could not log to Notion: {e}", "WARNING")
        improvement_record["notion_logged"] = False
    
    return improvement_record

def main():
    parser = argparse.ArgumentParser(description='Log continuous improvement')
    parser.add_argument('--department', required=True, help='Your department')
    parser.add_argument('--operation', required=True, help='What operation was improved')
    parser.add_argument('--improvement', required=True, help='What improvement was made')
    parser.add_argument('--impact', required=True, help='Measurable impact')
    parser.add_argument('--category', default='efficiency', 
                       choices=['efficiency', 'automation', 'quality', 'reusability', 'documentation', 'cost', 'simplification'])
    
    args = parser.parse_args()
    
    result = log_improvement(
        department=args.department,
        operation=args.operation,
        improvement=args.improvement,
        impact=args.impact,
        category=args.category
    )
    
    print("\n=== Improvement Logged ===")
    print(json.dumps(result, indent=2))
    print(f"\n✅ Keep improving!")

if __name__ == "__main__":
    main()
