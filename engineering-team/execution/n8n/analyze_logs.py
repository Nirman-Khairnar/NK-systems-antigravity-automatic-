#!/usr/bin/env python3
"""
Analyze n8n execution logs and suggest optimizations.
Uses OpenRouter API for intelligent analysis.
"""

import os
import json
import logging
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

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
    
    if model is None:
        model = os.getenv('OPENROUTER_MODEL', 'google/gemini-2.0-flash-exp:free')
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"OpenRouter API call failed: {e}")
        raise

def get_workflow_executions(workflow_id, hours=24):
    """Fetch execution history from n8n API."""
    api_url = os.getenv('N8N_API_URL', '').rstrip('/')
    api_key = os.getenv('N8N_API_KEY')
    
    if not api_url or not api_key:
        raise ValueError("N8N_API_URL and N8N_API_KEY must be set")
    
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        url = f"{api_url}/api/v1/executions"
        params = {
            "workflowId": workflow_id,
            "limit": 100
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        executions = response.json().get('data', [])
        logger.info(f"Retrieved {len(executions)} executions")
        
        return executions
        
    except Exception as e:
        logger.error(f"Failed to fetch executions: {e}")
        raise

def analyze_logs(workflow_id, hours=24, output_dir=".tmp"):
    """
    Analyze workflow executions and generate optimization suggestions.
    
    Args:
        workflow_id (str): n8n workflow ID
        hours (int): Hours of execution history to analyze
        output_dir (str): Directory to save reports
        
    Returns:
        dict: Performance report
    """
    logger.info(f"Analyzing logs for workflow {workflow_id}")
    
    # Fetch executions
    executions = get_workflow_executions(workflow_id, hours)
    
    if not executions:
        logger.warning("No executions found to analyze")
        return {"error": "No execution data available"}
    
    # Calculate metrics
    total = len(executions)
    successful = sum(1 for e in executions if e.get('finished') and not e.get('stoppedAt'))
    failed = total - successful
    success_rate = (successful / total * 100) if total > 0 else 0
    
    # Calculate average execution time
    durations = []
    for e in executions:
        if e.get('startedAt') and e.get('stoppedAt'):
            start = datetime.fromisoformat(e['startedAt'].replace('Z', '+00:00'))
            stop = datetime.fromisoformat(e['stoppedAt'].replace('Z', '+00:00'))
            duration = (stop - start).total_seconds()
            durations.append(duration)
    
    avg_duration = sum(durations) / len(durations) if durations else 0
    
    # Identify error patterns
    error_messages = []
    for e in executions:
        if e.get('data', {}).get('resultData', {}).get('error'):
            error_messages.append(e['data']['resultData']['error'])
    
    # Build performance report
    performance_report = {
        "workflow_id": workflow_id,
        "analysis_period_hours": hours,
        "total_executions": total,
        "successful_executions": successful,
        "failed_executions": failed,
        "success_rate_percent": round(success_rate, 2),
        "average_duration_seconds": round(avg_duration, 2),
        "error_count": len(error_messages),
        "sample_errors": error_messages[:5] if error_messages else []
    }
    
    # Save performance report
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "performance_report.json")
    with open(report_path, 'w') as f:
        json.dump(performance_report, f, indent=2)
    logger.info(f"Saved performance report to {report_path}")
    
    # Generate AI-powered optimization suggestions
    suggestions = generate_optimization_suggestions(performance_report, executions[:10])
    
    suggestions_path = os.path.join(output_dir, "optimization_suggestions.md")
    with open(suggestions_path, 'w') as f:
        f.write(suggestions)
    logger.info(f"Saved optimization suggestions to {suggestions_path}")
    
    return performance_report

def generate_optimization_suggestions(performance_report, sample_executions):
    """Use AI to analyze performance and suggest improvements."""
    
    prompt = f"""You are an n8n workflow optimization expert. Analyze this performance data and suggest specific improvements.

Performance Report:
{json.dumps(performance_report, indent=2)}

Sample Executions (most recent):
{json.dumps(sample_executions, indent=2)}

Provide actionable optimization suggestions in markdown format. Include:
1. Performance assessment (good/needs improvement)
2. Specific node-level optimizations
3. Error handling improvements
4. Scalability recommendations
5. Priority level (high/medium/low) for each suggestion

Be specific and practical. Focus on changes that can be implemented in n8n."""
    
    try:
        logger.info("Generating AI-powered optimization suggestions")
        response = call_openrouter(prompt)
        
        # Add header
        suggestions = f"""# Workflow Optimization Suggestions

**Workflow ID:** {performance_report['workflow_id']}  
**Analysis Period:** Last {performance_report['analysis_period_hours']} hours  
**Success Rate:** {performance_report['success_rate_percent']}%  
**Avg Duration:** {performance_report['average_duration_seconds']}s

---

{response}

---

*Generated by AI Analysis on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return suggestions
        
    except Exception as e:
        logger.error(f"Failed to generate suggestions: {e}")
        return f"# Optimization Analysis\n\nFailed to generate AI suggestions: {e}\n\nManual review recommended."

def main():
    """Main execution for testing."""
    import sys
    
    if len(sys.argv) < 2:
        # Try to load from deployment info
        deployment_path = ".tmp/deployment_info.json"
        if os.path.exists(deployment_path):
            with open(deployment_path, 'r') as f:
                deployment_info = json.load(f)
            workflow_id = deployment_info.get('workflow_id')
        else:
            print("Usage: python analyze_logs.py <workflow_id> [hours]")
            print("   or: ensure .tmp/deployment_info.json exists")
            sys.exit(1)
    else:
        workflow_id = sys.argv[1]
    
    hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    
    report = analyze_logs(workflow_id, hours)
    
    print("\n=== Performance Report ===")
    print(json.dumps(report, indent=2))
    print("\nSee .tmp/optimization_suggestions.md for detailed recommendations")

if __name__ == "__main__":
    main()
