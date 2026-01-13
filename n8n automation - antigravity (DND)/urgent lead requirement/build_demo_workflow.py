#!/usr/bin/env python3
"""
Rate Sourcing Demo - n8n Workflow Builder
Generates a production-ready n8n workflow that:
1. Accepts email text via Manual Trigger
2. Uses AI Agent + OpenAI to parse rate information
3. Structures the output as a clean JSON object
"""

import sys
import os

# Add parent directory to path to import n8n_builder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'execution'))
from n8n_builder import N8NWorkflow, N8NNode

def create_rate_sourcing_workflow():
    """Build the Rate Sourcing Demo workflow."""
    
    wf = N8NWorkflow("OTWL Rate Sourcing - AI Parser Demo")
    
    # 1. Manual Trigger (for demo purposes)
    trigger = wf.create_node(
        "Manual Trigger", 
        "n8n-nodes-base.manualTrigger",
        {}
    )
    
    # 2. Set Email Input (simulates receiving email text)
    # In the demo, user will paste one of the 3 mock emails here
    email_input = wf.create_node(
        "Email Input",
        "n8n-nodes-base.set",
        {
            "assignments": {
                "assignments": [
                    {
                        "id": "email_text",
                        "name": "email_text",
                        "value": "",  # User will manually paste email content during demo
                        "type": "string"
                    },
                    {
                        "id": "source_agent",
                        "name": "source_agent", 
                        "value": "Demo Agent",
                        "type": "string"
                    }
                ]
            }
        }
    )
    
    # 3. AI Agent - Parse Rate Information
    ai_agent = wf.create_node(
        "Extract Rate Data",
        "@n8n/n8n-nodes-langchain.agent",
        {
            "promptType": "define",
            "text": "={{ $json.email_text }}",
            "options": {
                "systemMessage": """You are a freight forwarding rate extraction specialist.

Your job: Extract shipping rate information from agent emails and return ONLY a valid JSON object.

Required fields (use "N/A" if not found):
{
  "agent_name": "Name of the agent/company",
  "ocean_freight_usd": "USD amount (number only, e.g., 2450)",
  "pol": "Port of Loading",
  "pod": "Port of Discharge", 
  "transit_time_days": "Transit time in days (number only)",
  "routing": "Shipping line/routing details",
  "valid_until": "Rate validity date",
  "earliest_etd": "Earliest departure date",
  "additional_charges": "Any extra charges mentioned"
}

CRITICAL: Return ONLY the JSON object. No explanations, no markdown, no extra text."""
            }
        }
    )
    
    # 4. OpenAI Chat Model (GPT-4o for accuracy)
    openai_model = wf.create_node(
        "OpenAI GPT-4o",
        "@n8n/n8n-nodes-langchain.lmChatOpenAi",
        {
            "model": {
                "__rl": True,
                "value": "gpt-4o",
                "mode": "id"
            },
            "options": {
                "temperature": 0.1  # Low temperature for consistent extraction
            }
        }
    )
    
    # 5. Format Output as Table
    format_output = wf.create_node(
        "Format as Table",
        "n8n-nodes-base.set",
        {
            "assignments": {
                "assignments": [
                    {
                        "id": "formatted_output",
                        "name": "formatted_summary",
                        "value": """=📊 EXTRACTED RATE INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent: {{ $json.output.agent_name }}
Ocean Freight: ${{ $json.output.ocean_freight_usd }}
Route: {{ $json.output.pol }} → {{ $json.output.pod }}
Transit: {{ $json.output.transit_time_days }} days
Carrier: {{ $json.output.routing }}
Valid Until: {{ $json.output.valid_until }}
Earliest ETD: {{ $json.output.earliest_etd }}
Extra Charges: {{ $json.output.additional_charges }}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""",
                        "type": "string"
                    }
                ]
            }
        }
    )
    
    # 6. Connections (Standard + AI topology)
    # Main flow
    wf.connect(trigger, email_input)
    wf.connect(email_input, ai_agent)
    wf.connect(ai_agent, format_output)
    
    # AI connections (star topology)
    wf.connect(openai_model, ai_agent, type="ai_languageModel")
    
    return wf

if __name__ == "__main__":
    workflow = create_rate_sourcing_workflow()
    
    # Save to file
    output_dir = os.path.join(os.path.dirname(__file__))
    output_path = os.path.join(output_dir, "rate_sourcing_demo_workflow.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(workflow.to_json())
    
    print("SUCCESS: Workflow generated successfully!")
    print(f"Saved to: {output_path}")
    print(f"\nNext steps:")
    print(f"1. Import this JSON into n8n")
    print(f"2. Add OpenAI credentials")
    print(f"3. Activate workflow")
    print(f"4. Paste demo_email_1.txt, demo_email_2.txt, or demo_email_3.txt into 'Email Input' node")
    print(f"5. Execute and show the parsed output!")


