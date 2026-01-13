#!/usr/bin/env python3
"""
Programmatically generate a complex 20+ node n8n workflow for Employee Onboarding.
This avoids AI generation parsing errors for large complex schemas.
"""

import json
import os

def build_workflow():
    nodes = []
    connections = {}
    
    # helper to add node and connection
    def add_node(name, type_name, position, params={}, credentials={}, id_suffix=None):
        node_id = str(len(nodes) + 1)
        nodes.append({
            "parameters": params,
            "id": node_id,
            "name": name,
            "type": type_name,
            "typeVersion": 1,
            "position": position,
            "credentials": credentials
        })
        return name

    def connect(source, target, index=0):
        if source not in connections:
            connections[source] = {"main": []}
        # Ensure main has enough lists
        while len(connections[source]["main"]) <= index:
            connections[source]["main"].append([])
        
        connections[source]["main"][index].append({
            "node": target,
            "type": "main",
            "index": 0
        })

    # 1. Trigger
    add_node("Manual Trigger", "n8n-nodes-base.manualTrigger", [200, 300])
    
    # 2. Validation
    add_node("Validate Email", "n8n-nodes-base.if", [400, 300], {
        "conditions": {
            "string": [{"value1": "={{$json.email}}", "operation": "contains", "value2": "@"}]
        }
    })
    connect("Manual Trigger", "Validate Email")
    
    # 3. Log Start
    add_node("Log Start", "n8n-nodes-base.googleSheets", [600, 300], {
        "operation": "append",
        "sheetId": "sheet123",
        "range": "A:E"
    }, {"googleSheetsApi": "Google Sheets Creds"})
    connect("Validate Email", "Log Start", 0) # True branch
    
    # 4. Switch (Dept)
    add_node("Route by Dept", "n8n-nodes-base.switch", [800, 300], {
        "dataType": "string",
        "value1": "={{$json.department}}",
        "rules": {
            "rules": [
                {"value2": "Engineering", "output": 0},
                {"value2": "Sales", "output": 1},
                {"value2": "Marketing", "output": 2}
            ]
        },
        "fallbackOutput": 3
    })
    connect("Log Start", "Route by Dept")
    
    # --- Branch 1: Engineering ---
    add_node("Create GitHub User", "n8n-nodes-base.httpRequest", [1000, 100], {
        "url": "https://api.github.com/users", "method": "POST"
    }, {"httpHeaderAuth": "GitHub Token"})
    connect("Route by Dept", "Create GitHub User", 0)
    
    add_node("Add to Jira", "n8n-nodes-base.httpRequest", [1200, 100], {
        "url": "https://jira.atlassian.com/users", "method": "POST"
    })
    connect("Create GitHub User", "Add to Jira")
    
    add_node("Slack Eng Channel", "n8n-nodes-base.slack", [1400, 100], {
        "channel": "engineering", "message": "New hire incoming!"
    })
    connect("Add to Jira", "Slack Eng Channel")
    
    add_node("Set Eng Equipment", "n8n-nodes-base.set", [1600, 100], {
        "values": {"string": [{"name": "equipment", "value": "MacBook Pro"}]}
    })
    connect("Slack Eng Channel", "Set Eng Equipment")
    
    # --- Branch 2: Sales ---
    add_node("Create Salesforce User", "n8n-nodes-base.httpRequest", [1000, 300], {
        "url": "https://salesforce.com/api/users", "method": "POST"
    })
    connect("Route by Dept", "Create Salesforce User", 1)
    
    add_node("Provision Zoom", "n8n-nodes-base.httpRequest", [1200, 300], {
        "url": "https://zoom.us/api/users", "method": "POST"
    })
    connect("Create Salesforce User", "Provision Zoom")
    
    add_node("Slack Sales Channel", "n8n-nodes-base.slack", [1400, 300], {
        "channel": "sales-wins", "message": "New seller joined!"
    })
    connect("Provision Zoom", "Slack Sales Channel")
    
    add_node("Set Sales Equipment", "n8n-nodes-base.set", [1600, 300], {
        "values": {"string": [{"name": "equipment", "value": "iPad, Laptop"}]}
    })
    connect("Slack Sales Channel", "Set Sales Equipment")
    
    # --- Branch 3: Marketing ---
    add_node("Create HubSpot User", "n8n-nodes-base.httpRequest", [1000, 500], {
        "url": "https://api.hubapi.com/owners", "method": "POST"
    })
    connect("Route by Dept", "Create HubSpot User", 2)
    
    add_node("Provision Canva", "n8n-nodes-base.httpRequest", [1200, 500], {
        "url": "https://api.canva.com/users", "method": "POST"
    })
    connect("Create HubSpot User", "Provision Canva")
    
    add_node("Slack Marketing Channel", "n8n-nodes-base.slack", [1400, 500], {
        "channel": "marketing", "message": "Creative team +1"
    })
    connect("Provision Canva", "Slack Marketing Channel")
    
    add_node("Set Mkt Equipment", "n8n-nodes-base.set", [1600, 500], {
        "values": {"string": [{"name": "equipment", "value": "Tablet"}]}
    })
    connect("Slack Marketing Channel", "Set Mkt Equipment")

    # --- Branch 4: HR (Default) ---
    add_node("BambooHR Access", "n8n-nodes-base.httpRequest", [1000, 700], {
         "url": "https://api.bamboohr.com", "method": "POST"
    })
    connect("Route by Dept", "BambooHR Access", 3)
    
    add_node("Set HR Equipment", "n8n-nodes-base.set", [1600, 700], {
        "values": {"string": [{"name": "equipment", "value": "Laptop"}]}
    })
    connect("BambooHR Access", "Set HR Equipment")

    # 5. Merge Branches
    add_node("Merge Validation", "n8n-nodes-base.merge", [1800, 300], {
        "mode": "append"
    })
    # Connect all branches to Merge
    connect("Set Eng Equipment", "Merge Validation", 0)
    connect("Set Sales Equipment", "Merge Validation", 0)
    connect("Set Mkt Equipment", "Merge Validation", 0)
    connect("Set HR Equipment", "Merge Validation", 0)
    
    # 6. Final Steps
    add_node("Create Google Account", "n8n-nodes-base.googleWorkspaceAdmin", [2000, 300], {
        "resource": "user", "operation": "create", "email": "={{$json.email}}"
    })
    connect("Merge Validation", "Create Google Account")
    
    add_node("Send Welcome Email", "n8n-nodes-base.gmail", [2200, 300], {
        "resource": "message", "operation": "send", "message": "Welcome!", "toEmail": "={{$json.email}}"
    })
    connect("Create Google Account", "Send Welcome Email")
    
    add_node("Final Log", "n8n-nodes-base.googleSheets", [2400, 300], {
        "operation": "append", "sheetId": "sheet123", "range": "F:F"
    })
    connect("Send Welcome Email", "Final Log")
    
    # 7. Error Handler
    add_node("Error Trigger", "n8n-nodes-base.errorTrigger", [400, 600])
    
    add_node("Post Error to Slack", "n8n-nodes-base.slack", [600, 600], {
        "channel": "it-support", "message": "Workflow Error: {{$execution.id}}"
    })
    connect("Error Trigger", "Post Error to Slack")

    # Build final JSON
    workflow = {
        "name": "Employee Onboarding (Complex)",
        "nodes": nodes,
        "connections": connections,
        "active": False,
        "settings": {},
        "tags": []
    }
    
    # Output to .tmp
    os.makedirs(".tmp", exist_ok=True)
    with open(".tmp/workflow.json", "w") as f:
        json.dump(workflow, f, indent=2)
    
    print(f"Generated workflow with {len(nodes)} nodes in .tmp/workflow.json")

if __name__ == "__main__":
    build_workflow()
