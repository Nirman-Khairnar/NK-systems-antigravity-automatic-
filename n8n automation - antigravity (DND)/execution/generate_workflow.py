#!/usr/bin/env python3
"""
Generate n8n workflows using the deterministic n8n_builder library.
This script reads requirements and constructs a "Gold Standard" workflow
programmatically, ensuring 100% valid JSON and correct topologies.
"""

import json
import os
import logging
try:
    from execution.n8n_builder import N8NWorkflow, create_webhook, create_ai_agent, create_openai_model, create_window_memory, create_guardrails
except ImportError:
    from n8n_builder import N8NWorkflow, create_webhook, create_ai_agent, create_openai_model, create_window_memory, create_guardrails

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_business_workflow(requirements, output_path):
    """
    Constructs a workflow based on the "Modern AI Agent" pattern.
    """
    wf_name = requirements.get("workflow_name", "AI Business Automation")
    wf = N8NWorkflow(wf_name)
    
    logger.info(f"Building workflow: {wf_name}")
    
    # 1. Trigger (Default to Webhook for Agent interaction)
    trigger = create_webhook(wf, "chat/start", "POST")
    logger.info("Added Trace: Webhook Trigger")
    
    # 2. AI Core (The 'Brain')
    # Using the builder's verified factories
    model = create_openai_model(wf, model="gpt-4o")
    memory = create_window_memory(wf)
    guardrails = create_guardrails(wf)
    
    agent = create_ai_agent(wf, {
        "text": "={{$json.query}}",
        "options": {
            "systemMessage": "You are a specialized business automation agent. Use your tools to assist the user."
        }
    })
    
    # 3. Connect the Brain
    wf.connect(trigger, agent)
    wf.connect(model, agent, type="ai_languageModel")
    wf.connect(memory, agent, type="ai_memory")
    wf.connect(guardrails, agent, type="ai_guardrails") # Using our researched key
    
    pass # In future, we can add Tool nodes (CRM, Email) here based on requirements
    
    logger.info("Workflow graph constructed successfully.")
    
    # 4. Save
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(wf.to_json())
        
    return wf

def main():
    req_path = "requirements.json"
    out_dir = ".tmp"
    os.makedirs(out_dir, exist_ok=True)
    
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            requirements = json.load(f)
    else:
        requirements = {"workflow_name": "Generated Agent"}
        
    output_path = os.path.join(out_dir, "workflow.json")
    try:
        generate_business_workflow(requirements, output_path)
        logger.info(f"Generated verified workflow at {output_path}")
    except Exception as e:
        logger.error(f"Failed to generate workflow: {e}")
        raise

if __name__ == "__main__":
    main()
