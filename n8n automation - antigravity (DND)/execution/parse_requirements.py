#!/usr/bin/env python3
"""
Parse natural language requirements into structured JSON.
Uses OpenRouter API (free Gemini model) for intelligent extraction.
"""

import os
import json
import logging
from dotenv import load_dotenv
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def call_openrouter(prompt, model=None):
    """Call OpenRouter API with the given prompt."""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment")
    
    # Use free Gemini model if not specified
    if model is None:
        model = os.getenv('OPENROUTER_MODEL', 'google/gemini-2.0-flash-exp:free')
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"OpenRouter API call failed: {e}")
        raise

def parse_requirements(requirements_text, output_dir=".tmp"):
    """
    Parse natural language requirements into structured JSON.
    
    Args:
        requirements_text (str): Raw requirements from client
        output_dir (str): Directory to save output files
        
    Returns:
        dict: Structured requirements data
    """
    logger.info("Starting requirements parsing")
    
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    # Build prompt for AI extraction
    prompt = f"""You are an expert n8n workflow analyst. Extract structured information from these client requirements.

Requirements:
{requirements_text}

Extract the following and return ONLY valid JSON (no markdown, no explanation):
{{
    "workflow_name": "brief descriptive name",
    "goal": "what the workflow accomplishes",
    "triggers": [
        {{
            "type": "webhook|schedule|manual|event",
            "description": "when this triggers",
            "configuration": {{}}
        }}
    ],
    "data_sources": [
        {{
            "name": "API/service name",
            "purpose": "what data is being accessed",
            "credentials_needed": true/false
        }}
    ],
    "actions": [
        {{
            "step": 1,
            "description": "what happens",
            "node_type": "HTTP Request|Google Sheets|Slack|etc"
        }}
    ],
    "data_transformations": [
        {{
            "description": "how data is transformed",
            "input": "source field",
            "output": "target field"
        }}
    ],
    "error_handling": {{
        "strategy": "retry|notify|fallback|stop",
        "notification_method": "slack|email|webhook|none"
    }},
    "success_metrics": "how to measure success",
    "missing_info": [
        "list any critical information not provided in requirements"
    ]
}}"""
    
    try:
        # Call AI to extract structure
        logger.info("Calling OpenRouter API for extraction")
        response = call_openrouter(prompt)
        
        # Parse JSON response
        # Remove markdown code blocks if present
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        structured_data = json.loads(response)
        
        # Save structured requirements
        requirements_path = os.path.join(output_dir, "requirements.json")
        with open(requirements_path, 'w') as f:
            json.dump(structured_data, f, indent=2)
        logger.info(f"Saved structured requirements to {requirements_path}")
        
        # Check if there's missing info - generate questions
        if structured_data.get('missing_info') and len(structured_data['missing_info']) > 0:
            questions = generate_clarifying_questions(structured_data)
            questions_path = os.path.join(output_dir, "questions.json")
            with open(questions_path, 'w') as f:
                json.dump(questions, f, indent=2)
            logger.info(f"Generated clarifying questions in {questions_path}")
        
        return structured_data
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response as JSON: {e}")
        logger.error(f"Response was: {response}")
        raise
    except Exception as e:
        logger.error(f"Requirements parsing failed: {e}")
        raise

def generate_clarifying_questions(structured_data):
    """Generate prioritized clarifying questions based on missing info."""
    missing = structured_data.get('missing_info', [])
    
    prompt = f"""Based on this workflow analysis, generate clarifying questions for the client.

Workflow: {structured_data.get('workflow_name')}
Missing Information: {json.dumps(missing, indent=2)}

Generate questions prioritized by importance (blocking vs. nice-to-have).
Return ONLY valid JSON:
{{
    "blocking_questions": [
        {{
            "question": "specific question",
            "reason": "why this is critical",
            "suggested_default": "reasonable default if client doesn't respond"
        }}
    ],
    "optional_questions": [
        {{
            "question": "specific question",
            "reason": "why this would be helpful"
        }}
    ]
}}"""
    
    try:
        response = call_openrouter(prompt)
        
        # Clean response
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        return json.loads(response)
    except Exception as e:
        logger.error(f"Failed to generate questions: {e}")
        return {"blocking_questions": [], "optional_questions": []}

def main():
    """Main execution for testing."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python parse_requirements.py <requirements_file>")
        print("   or: python parse_requirements.py '<requirements text>'")
        sys.exit(1)
    
    # Check if argument is a file or text
    arg = sys.argv[1]
    if os.path.isfile(arg):
        with open(arg, 'r') as f:
            requirements = f.read()
    else:
        requirements = arg
    
    # Parse requirements
    result = parse_requirements(requirements)
    
    print("\n=== Structured Requirements ===")
    print(json.dumps(result, indent=2))
    
    # Check for questions
    if os.path.exists(".tmp/questions.json"):
        with open(".tmp/questions.json", 'r') as f:
            questions = json.load(f)
        print("\n=== Clarifying Questions Required ===")
        print(json.dumps(questions, indent=2))

if __name__ == "__main__":
    main()
