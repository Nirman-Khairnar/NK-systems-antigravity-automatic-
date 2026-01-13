#!/usr/bin/env python3
"""
OTWL Rate Management Workflow Builder
Comprehensive workflow covering Steps 3-10 of OTWL's freight forwarding process.

Features:
- Gmail triggers for customer inquiries and agent responses
- AI-powered rate extraction (reuses demo logic)
- Google Sheets integration for tracking
- Automated quotation generation
- Customer follow-up system
"""

import sys
import os

# Add parent directory to path to import n8n_builder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'execution'))
from n8n_builder import N8NWorkflow, N8NNode

def create_otwl_rate_workflow():
    """Build the comprehensive OTWL Rate Management workflow."""
    
    wf = N8NWorkflow("OTWL Rate Management - Steps 3-10")
    wf.current_y = 0  # Reset Y position for better layout
    
    # ==================== PART 1: Customer Inquiry Flow ====================
    
    # Trigger 1: Gmail - Customer Inquiry
    gmail_trigger_inquiry = wf.create_node(
        "Customer Inquiry Received",
        "n8n-nodes-base.gmailTrigger",
        {
            "pollTimes": {
                "item": [
                    {"mode": "everyMinute"}
                ]
            },
            "filters": {
                "subject": "rate request,quotation,freight quote",
                "includeSpam": False
            },
            "options": {}
        }
    )
    
    # Extract customer details from email
    extract_inquiry = wf.create_node(
        "Extract Inquiry Details",
        "n8n-nodes-base.code",
        {
            "mode": "runOnceForAllItems",
            "jsCode": """
// Extract customer inquiry details from email
const email = $input.all()[0].json;

return {
  inquiry_id: 'INQ-' + new Date().getTime() + '-' + Math.random().toString(36).substr(2, 4).toUpperCase(),
  customer_email: email.from,
  customer_name: email.from.split('<')[0].trim(),
  subject: email.subject,
  body: email.textPlain || email.snippet,
  received_date: new Date().toISOString(),
  status: 'pending_rates'
};
"""
        }
    )
    
    # Send auto-reply to customer
    send_autoreply = wf.create_node(
        "Send Auto-Reply to Customer",
        "n8n-nodes-base.gmail",
        {
            "resource": "message",
            "operation": "send",
            "to": "={{ $json.customer_email }}",
            "subject": "Re: {{ $json.subject }}",
            "message": """Dear {{ $json.customer_name }},

Thank you for your inquiry. We have received your rate request and are currently sourcing quotes from our network of agents.

You can expect to receive our competitive quotation within 24-48 hours.

Inquiry Reference: {{ $json.inquiry_id }}

Best regards,
Ocean Transworld Logistics Team""",
            "options": {}
        }
    )
    
    # Log inquiry in Google Sheets
    log_inquiry = wf.create_node(
        "Log Inquiry in Sheets",
        "n8n-nodes-base.googleSheets",
        {
            "operation": "append",
            "sheetId": {
                "__rl": True,
                "value": "inquiries",
                "mode": "list"
            },
            "columns": {
                "mappingMode": "defineBelow",
                "value": {
                    "inquiry_id": "={{ $json.inquiry_id }}",
                    "customer_email": "={{ $json.customer_email }}",
                    "customer_name": "={{ $json.customer_name }}",
                    "subject": "={{ $json.subject }}",
                    "received_date": "={{ $json.received_date }}",
                    "status": "={{ $json.status }}"
                }
            },
            "options": {}
        }
    )
    
    # Get agent list from Google Sheets
    get_agents = wf.create_node(
        "Get Agent List",
        "n8n-nodes-base.googleSheets",
        {
            "operation": "read",
            "sheetId": {
                "__rl": True,
                "value": "agents",
                "mode": "list"
            },
            "options": {
                "range": "A2:C100"
            }
        }
    )
    
    # Send rate request to agents (using Loop)
    send_to_agents = wf.create_node(
        "Send Rate Request to Agents",
        "n8n-nodes-base.gmail",
        {
            "resource": "message",
            "operation": "send",
            "to": "={{ $json.agent_email }}",
            "subject": "Rate Request - {{ $('Extract Inquiry Details').item.json.inquiry_id }}",
            "message": """Dear {{ $json.agent_name }},

We are requesting a freight quote for the following shipment:

Reference: {{ $('Extract Inquiry Details').item.json.inquiry_id }}
Customer: {{ $('Extract Inquiry Details').item.json.customer_name }}

Please provide your best rates including:
- Ocean Freight (USD per container)
- Port of Loading (POL)
- Port of Discharge (POD)
- Transit Time
- Routing/Carrier
- Rate Validity
- Earliest ETD

Please respond to this email with your quote at the earliest.

Best regards,
OTWL Team""",
            "options": {}
        }
    )
    
    # ==================== PART 2: Agent Response Flow ====================
    
    # Reset Y position for second flow
    wf.current_y = 400
    wf.current_x = 0
    
    # Trigger 2: Gmail - Agent Responses
    gmail_trigger_agent = wf.create_node(
        "Agent Response Received",
        "n8n-nodes-base.gmailTrigger",
        {
            "pollTimes": {
                "item": [
                    {"mode": "everyMinute"}
                ]
            },
            "filters": {
                "subject": "INQ-,Rate Request",
                "includeSpam": False
            },
            "options": {}
        }
    )
    
    # Extract inquiry_id from subject
    extract_inquiry_id = wf.create_node(
        "Extract Inquiry ID",
        "n8n-nodes-base.code",
        {
            "mode": "runOnceForAllItems",
            "jsCode": """
const email = $input.all()[0].json;
const subject = email.subject;
const match = subject.match(/INQ-\\d+-[A-Z0-9]+/);

return {
  inquiry_id: match ? match[0] : 'UNKNOWN',
  agent_email: email.from,
  email_body: email.textPlain || email.snippet,
  received_date: new Date().toISOString()
};
"""
        }
    )
    
    # AI Agent - Parse Rate (REUSE FROM DEMO)
    parse_rate = wf.create_node(
        "AI Parse Rate Data",
        "@n8n/n8n-nodes-langchain.agent",
        {
            "promptType": "define",
            "text": "={{ $json.email_body }}",
            "options": {
                "systemMessage": """You are a freight forwarding rate extraction specialist.

Extract shipping rate information and return ONLY a valid JSON object.

Required fields (use "N/A" if not found):
{
  "agent_name": "Name of agent/company",
  "ocean_freight_usd": "USD amount (number only)",
  "pol": "Port of Loading",
  "pod": "Port of Discharge",
  "transit_time_days": "Transit days (number only)",
  "routing": "Shipping line/routing",
  "valid_until": "Rate validity date",
  "earliest_etd": "Earliest departure date",
  "additional_charges": "Extra charges"
}

CRITICAL: Return ONLY the JSON object. No explanations."""
            }
        }
    )
    
    # OpenAI Model for AI Agent
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
                "temperature": 0.1
            }
        }
    )
    
    # Append rate to Google Sheets
    append_rate = wf.create_node(
        "Append Rate to Sheets",
        "n8n-nodes-base.googleSheets",
        {
            "operation": "append",
            "sheetId": {
                "__rl": True,
                "value": "agent_rates",
                "mode": "list"
            },
            "columns": {
                "mappingMode": "defineBelow",
                "value": {
                    "inquiry_id": "={{ $('Extract Inquiry ID').item.json.inquiry_id }}",
                    "agent_name": "={{ $json.output.agent_name }}",
                    "ocean_freight_usd": "={{ $json.output.ocean_freight_usd }}",
                    "pol": "={{ $json.output.pol }}",
                    "pod": "={{ $json.output.pod }}",
                    "transit_time_days": "={{ $json.output.transit_time_days }}",
                    "routing": "={{ $json.output.routing }}",
                    "valid_until": "={{ $json.output.valid_until }}",
                    "earliest_etd": "={{ $json.output.earliest_etd }}",
                    "received_date": "={{ $('Extract Inquiry ID').item.json.received_date }}"
                }
            },
            "options": {}
        }
    )
    
    # Check if all agents responded (using Google Sheets lookup)
    check_rates = wf.create_node(
        "Check Rate Count",
        "n8n-nodes-base.googleSheets",
        {
            "operation": "read",
            "sheetId": {
                "__rl": True,
                "value": "agent_rates",
                "mode": "list"
            },
            "filters": {
                "conditions": {
                    "inquiry_id": "={{ $('Extract Inquiry ID').item.json.inquiry_id }}"
                }
            },
            "options": {}
        }
    )
    
    # IF node - Check if we have at least 3 rates
    if_enough_rates = wf.create_node(
        "Have 3+ Rates?",
        "n8n-nodes-base.if",
        {
            "conditions": {
                "conditions": [
                    {
                        "leftValue": "={{ $json.length }}",
                        "operation": "largerEqual",
                        "rightValue": 3
                    }
                ]
            }
        }
    )
    
    # Generate quotation (sort rates, pick top 3)
    generate_quote = wf.create_node(
        "Generate Quotation",
        "n8n-nodes-base.code",
        {
            "mode": "runOnceForAllItems",
            "jsCode": """
const rates = $input.all().map(item => item.json);

// Sort by price (lowest first)
const sorted = rates.sort((a, b) => 
  parseFloat(a.ocean_freight_usd) - parseFloat(b.ocean_freight_usd)
);

const top3 = sorted.slice(0, 3);

return {
  inquiry_id: rates[0].inquiry_id,
  top_rates: top3,
  quotation_text: top3.map((r, i) => 
    `Option ${i+1}: ${r.agent_name}
    Rate: $${r.ocean_freight_usd}
    Route: ${r.pol} → ${r.pod}
    Transit: ${r.transit_time_days} days
    Carrier: ${r.routing}
    Valid Until: ${r.valid_until}
    `
  ).join('\\n---\\n')
};
"""
        }
    )
    
    # Send quotation to customer
    send_quotation = wf.create_node(
        "Send Quotation to Customer",
        "n8n-nodes-base.gmail",
        {
            "resource": "message",
            "operation": "send",
            "to": "={{ $('Extract Inquiry Details').item.json.customer_email }}",
            "subject": "Quotation - {{ $json.inquiry_id }}",
            "message": """Dear Customer,

Thank you for your patience. We have received competitive rates from our agents.

Here are our top 3 options:

{{ $json.quotation_text }}

Please review and let us know which option you would like to proceed with.

Best regards,
Ocean Transworld Logistics Team""",
            "options": {}
        }
    )
    
    # Log quotation sent
    log_quotation = wf.create_node(
        "Log Quotation Sent",
        "n8n-nodes-base.googleSheets",
        {
            "operation": "append",
            "sheetId": {
                "__rl": True,
                "value": "quotations",
                "mode": "list"
            },
            "columns": {
                "mappingMode": "defineBelow",
                "value": {
                    "inquiry_id": "={{ $json.inquiry_id }}",
                    "quote_sent_date": "={{ new Date().toISOString() }}",
                    "status": "pending_customer_response"
                }
            }
        }
    )
    
    # ==================== Connections ====================
    
    # Flow 1: Customer Inquiry
    wf.connect(gmail_trigger_inquiry, extract_inquiry)
    wf.connect(extract_inquiry, send_autoreply)
    wf.connect(send_autoreply, log_inquiry)
    wf.connect(log_inquiry, get_agents)
    wf.connect(get_agents, send_to_agents)
    
    # Flow 2: Agent Response
    wf.connect(gmail_trigger_agent, extract_inquiry_id)
    wf.connect(extract_inquiry_id, parse_rate)
    wf.connect(parse_rate, append_rate)
    wf.connect(append_rate, check_rates)
    wf.connect(check_rates, if_enough_rates)
    wf.connect(if_enough_rates, generate_quote)
    wf.connect(generate_quote, send_quotation)
    wf.connect(send_quotation, log_quotation)
    
    # AI Connection
    wf.connect(openai_model, parse_rate, type="ai_languageModel")
    
    return wf

if __name__ == "__main__":
    workflow = create_otwl_rate_workflow()
    
    # Save to file
    output_dir = os.path.join(os.path.dirname(__file__))
    output_path = os.path.join(output_dir, "otwl_rate_management_workflow.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(workflow.to_json())
    
    print("SUCCESS: OTWL Rate Management workflow generated!")
    print(f"Saved to: {output_path}")
    print(f"\nWorkflow includes:")
    print(f"- Gmail triggers for customer inquiries and agent responses")
    print(f"- AI-powered rate extraction (GPT-4o)")
    print(f"- Google Sheets integration (3 sheets: inquiries, agent_rates, quotations)")
    print(f"- Automated quotation generation")
    print(f"- Status tracking throughout the process")
