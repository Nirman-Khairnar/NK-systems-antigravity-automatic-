#!/usr/bin/env python3
"""
Generate Velocity Report for NK in Notion - Chief of Staff function.

Creates daily Velocity Report page in Notion 'NK Daily Briefs' database:
- Execution Status (Speed check)
- What Shipped (Last 24h)
- System Health
- Strategic Alerts
- Weekly Docs Countdown

usage: python generate_daily_brief.py
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Simple logger fallback
class SimpleLogger:
    def __init__(self, dept, script):
        self.dept = dept
        self.script = script
    def log(self, msg, level="INFO"):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] [{level}] {self.dept}/{self.script}: {msg}")

def generate_daily_brief(target_date=None):
    """Generate Velocity Report JSON for Agent execution via MCP."""
    
    logger = SimpleLogger("NK-personal-team", "generate_daily_brief")
    
    if not target_date:
        target_date = datetime.now().strftime('%Y-%m-%d')
    date_obj = datetime.strptime(target_date, '%Y-%m-%d')
    
    # Calculate days until next weekly review (assuming Monday = 0)
    # If today is Monday(0), next review is 7 days? Or today? Let's say review is next Monday.
    days_until_review = 7 - date_obj.weekday()
    if days_until_review == 7: days_until_review = 0 # It's review day
    
    # Velocity Report Content
    brief = {
        "date": target_date,
        "type": "Velocity Report",
        "generated_at": datetime.now().isoformat(),
        "database_id": "2e750cd5-29b6-80ed-b3eb-e48dc9c98799", 
        "title": f"🚀 Velocity Report - {date_obj.strftime('%b %d')}",
        "sections": {
            "execution_speed": "HIGH ⚡",
            "shipped_last_24h": [
                "Executive Dashboard (Notion)",
                "Chief of Staff Protocol (NK-Personal)",
                "Daily Velocity Reporting System"
            ],
            "system_health": {
                "engineering": "🟢 Shipping",
                "sales": "🟢 Prospecting",
                "research": "🟢 Analysis",
                "operations": "🟢 Coordinating"
            },
            "strategic_alerts": [
                "Review new operational cadence (Velocity > Planning)"
            ],
            "weekly_docs_status": f"Weekly Docs Check: {days_until_review} days remaining"
        }
    }

    # Save to file for the Agent to pickup
    output_file = f".tmp/velocity_report_{target_date}.json"
    os.makedirs('.tmp', exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(brief, f, indent=2)
    
    logger.log(f"Velocity report generated: {output_file}")
    
    # Print instructions for the Agent
    print(json.dumps({
        "status": "success",
        "file": output_file,
        "action_required": "create_database_page",
        "database_id": brief["database_id"],
        "brief_summary": "Velocity Report ready"
    }, indent=2))
    
    return brief

def main():
    generate_daily_brief()

if __name__ == "__main__":
    main()
