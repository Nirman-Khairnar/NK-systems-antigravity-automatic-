#!/usr/bin/env python3
"""
Master orchestrator for agentic n8n workflow system.
Runs the complete pipeline: requirements → workflow → deployment → documentation
Adapted for Antigravity Organization Structure.
"""

import os
import sys
import json
import logging
from datetime import datetime

# Add n8n subdirectory to path so imports work
# Current file is in D:\NK systems (antigravity) DND\engineering-team\execution\n8n_pipeline.py
# Scripts are in D:\NK systems (antigravity) DND\engineering-team\execution\n8n\
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'n8n'))

from parse_requirements import parse_requirements
# FIXED: Import the correct function
from generate_workflow import generate_business_workflow
from deploy_to_n8n import deploy_to_n8n
from create_notion_docs import create_notion_docs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_pipeline(requirements_text, deploy=True, document=True, project_name=None):
    """
    Run the complete agentic workflow pipeline.
    
    Args:
        requirements_text (str): Natural language requirements
        deploy (bool): Whether to deploy to n8n
        document (bool): Whether to create Notion docs
        project_name (str): Optional project name for output directory
        
    Returns:
        dict: Pipeline results
    """
    logger.info("=" * 60)
    logger.info("ANTIGRAVITY N8N PIPELINE - ENGINEERING TEAM")
    logger.info("=" * 60)
    
    # Create project directory in root .tmp
    if project_name is None:
        project_name = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    output_dir = os.path.join(".tmp", project_name)
    os.makedirs(output_dir, exist_ok=True)
    
    results = {
        "project_name": project_name,
        "output_dir": output_dir,
        "stages": {}
    }
    
    try:
        # STAGE 1: Requirements Validation
        logger.info("\n" + "=" * 60)
        logger.info("STAGE 1: REQUIREMENTS VALIDATION")
        logger.info("=" * 60)
        
        requirements_data = parse_requirements(requirements_text, output_dir)
        results["stages"]["requirements"] = {
            "status": "success",
            "output": f"{output_dir}/requirements.json"
        }
        
        # Check if questions were generated
        questions_path = os.path.join(output_dir, "questions.json")
        if os.path.exists(questions_path):
            with open(questions_path, 'r') as f:
                questions = json.load(f)
            
            logger.warning("CLARIFYING QUESTIONS NEEDED:")
            for q in questions.get('blocking_questions', []):
                logger.warning(f"  - {q['question']}")
            
            results["stages"]["requirements"]["questions"] = questions
            results["stages"]["requirements"]["status"] = "needs_clarification"
            
            # Stop pipeline - need user input
            logger.info("\nPipeline paused: User clarification required")
            return results
        
        logger.info(f"✓ Requirements validated: {requirements_data.get('workflow_name')}")
        
        # STAGE 2: Workflow Generation
        logger.info("\n" + "=" * 60)
        logger.info("STAGE 2: WORKFLOW GENERATION")
        logger.info("=" * 60)
        
        req_path = os.path.join(output_dir, "requirements.json")
        wf_output_path = os.path.join(output_dir, "workflow.json")
        
        # Load requirements dict
        with open(req_path, 'r') as f:
            requirements = json.load(f)
            
        # Call the actual generation function
        wf = generate_business_workflow(requirements, wf_output_path)
        
        # Parse the output to get node count for reporting
        workflow_data = json.loads(wf.to_json())
        
        results["stages"]["workflow_generation"] = {
            "status": "success",
            "output": wf_output_path,
            "node_count": len(workflow_data.get('nodes', []))
        }
        
        logger.info(f"✓ Workflow generated: {len(workflow_data.get('nodes', []))} nodes")
        
        # STAGE 3: Deployment (optional)
        if deploy:
            logger.info("\n" + "=" * 60)
            logger.info("STAGE 3: MVP DEPLOYMENT")
            logger.info("=" * 60)
            
            deployment_info = deploy_to_n8n(wf_output_path, "staging", output_dir)
            results["stages"]["deployment"] = {
                "status": "success",
                "workflow_id": deployment_info.get('workflow_id'),
                "environment": "staging"
            }
            
            logger.info(f"✓ Deployed to n8n: {deployment_info.get('workflow_id')}")
            logger.warning("⚠ MANUAL STEP REQUIRED: Configure credentials in n8n UI")
        
        # STAGE 4: Documentation (optional)
        if document:
            logger.info("\n" + "=" * 60)
            logger.info("STAGE 4: NOTION DOCUMENTATION")
            logger.info("=" * 60)
            
            deploy_path = os.path.join(output_dir, "deployment_info.json")
            
            page_info = create_notion_docs(
                req_path, 
                wf_output_path,
                deploy_path if deploy else None,
                None,  # No performance data yet
                output_dir
            )
            
            results["stages"]["documentation"] = {
                "status": "success",
                "page_url": page_info.get('page_url')
            }
            
            logger.info(f"✓ Documentation created: {page_info.get('page_url')}")
        
        # Pipeline complete
        logger.info("\n" + "=" * 60)
        logger.info("PIPELINE COMPLETE")
        logger.info("=" * 60)
        
        results["status"] = "success"
        results["completion_time"] = datetime.now().isoformat()
        
        return results
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        results["status"] = "error"
        results["error"] = str(e)
        raise

def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Antigravity Engineering: n8n Workflow Pieline')
    parser.add_argument('requirements', help='Requirements text or file path')
    parser.add_argument('--no-deploy', action='store_true', help='Skip n8n deployment')
    parser.add_argument('--no-docs', action='store_true', help='Skip Notion documentation')
    parser.add_argument('--project-name', help='Project name for output directory')
    
    args = parser.parse_args()
    
    # Load requirements
    if os.path.isfile(args.requirements):
        with open(args.requirements, 'r') as f:
            requirements = f.read()
    else:
        requirements = args.requirements
    
    # Run pipeline
    results = run_pipeline(
        requirements,
        deploy=not args.no_deploy,
        document=not args.no_docs,
        project_name=args.project_name
    )
    
    # Print results
    print("\n" + "=" * 60)
    print("PIPELINE RESULTS")
    print("=" * 60)
    print(json.dumps(results, indent=2))
    
    if results.get('status') == 'success':
        print("\n✅ All stages completed successfully!")
        if 'documentation' in results['stages']:
            print(f"\n📄 View documentation: {results['stages']['documentation']['page_url']}")
    elif results['stages']['requirements'].get('status') == 'needs_clarification':
        print("\n⚠️ Pipeline paused - clarification needed")
        print(f"See {results['output_dir']}/questions.json")

if __name__ == "__main__":
    main()
