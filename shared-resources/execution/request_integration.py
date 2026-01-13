#!/usr/bin/env python3
"""
Request integration of new tool/service - User approval workflow.

Usage:
    python request_integration.py --tool "Airtable" --purpose "Client needs data in Airtable" --urgency "high"
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

def request_integration(tool_name, purpose, alternatives="None", urgency="medium", estimated_cost="Unknown"):
    """
    Request integration of new tool - requires user approval.
    
    Args:
        tool_name (str): Name of tool to integrate
        purpose (str): Why we need it
        alternatives (str): What we use now
        urgency (str): How urgent (blocking, high, medium, low)
        estimated_cost (str): Cost estimate (Free, $XX/month, etc.)
        
    Returns:
        dict: Integration request record
    """
    logger = CentralLogger("engineering-team", "request_integration")
    
    request_id = f"int-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    request_record = {
        "request_id": request_id,
        "tool_name": tool_name,
        "purpose": purpose,
        "alternatives": alternatives,
        "urgency": urgency,
        "estimated_cost": estimated_cost,
        "requested_by": "engineering-team",
        "timestamp": datetime.now().isoformat(),
        "status": "pending_approval"
    }
    
    # Log
    logger.log(f"INTEGRATION REQUEST: {tool_name} - {purpose} [Urgency: {urgency}]")
    
    # Save request
    os.makedirs('.tmp', exist_ok=True)
    with open(f'.tmp/integration_request_{request_id}.json', 'w') as f:
        json.dump(request_record, f, indent=2)
    
    # Append to requests log
    with open('.tmp/integration_requests.jsonl', 'a') as f:
        f.write(json.dumps(request_record) + '\n')
    
    # Print user-facing request
    print(f"\n{'='*60}")
    print(f"🔧 INTEGRATION REQUEST - USER APPROVAL NEEDED")
    print(f"{'='*60}\n")
    print(f"Tool: {tool_name}")
    print(f"Purpose: {purpose}")
    print(f"Current Alternative: {alternatives}")
    print(f"Urgency: {urgency.upper()}")
    print(f"Estimated Cost: {estimated_cost}\n")
    print(f"Request ID: {request_id}")
    print(f"Requested: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Flag for orchestrator
    with open('.tmp/INTEGRATION_REQUEST.flag', 'w') as f:
        f.write(request_id)
    
    return request_record

def main():
    parser = argparse.ArgumentParser(description='Request new tool integration')
    parser.add_argument('--tool', required=True, help='Tool name to integrate')
    parser.add_argument('--purpose', required=True, help='Why we need this tool')
    parser.add_argument('--alternatives', default='None', help='What we use currently')
    parser.add_argument('--urgency', default='medium', choices=['blocking', 'high', 'medium', 'low'])
    parser.add_argument('--cost', default='Unknown', help='Estimated cost (Free, $XX/month)')
    
    args = parser.parse_args()
    
    result = request_integration(
        tool_name=args.tool,
        purpose=args.purpose,
        alternatives=args.alternatives,
        urgency=args.urgency,
        estimated_cost=args.cost
    )
    
    print(f"✅ Integration request created: {result['request_id']}")
    print(f"📁 Logged to: .tmp/integration_request_{result['request_id']}.json")
    print(f"\n⏳ Awaiting user approval...")

if __name__ == "__main__":
    main()
