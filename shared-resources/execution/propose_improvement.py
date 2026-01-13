#!/usr/bin/env python3
"""
Propose improvements or challenges to user proposals.
Departments use this to submit structured feedback.

Usage:
    python propose_improvement.py --proposal-id "prop-123" --department "engineering-team" --type "better_alternative"
"""

import os
import sys
import json
import argparse
import uuid
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from shared_resources.execution.logger import CentralLogger

load_dotenv()

def propose_improvement(proposal_id, department, challenge_type, description, 
                       risks=None, alternative=None, impact=None, reasoning="", 
                       recommendation="approve_with_changes", confidence="high"):
    """
    Submit a structured improvement proposal or challenge.
    
    Args:
        proposal_id (str): ID of the proposal being challenged
        department (str): Department submitting the challenge
        challenge_type (str): Type of feedback
        description (str): Description of the challenge/improvement
        risks (list): List of identified risks
        alternative (dict): Alternative approach details
        impact (dict): Impact analysis (time, cost, quality)
        reasoning (str): First-principles explanation
        recommendation (str): Department's recommendation
        confidence (str): Confidence level
        
    Returns:
        dict: Challenge record
    """
    logger = CentralLogger(department, "propose_improvement")
    
    challenge_id = str(uuid.uuid4())[:8]
    
    # Build challenge according to schema
    challenge = {
        "challenge_id": challenge_id,
        "proposal_id": proposal_id,
        "department": department,
        "timestamp": datetime.now().isoformat(),
        "challenge_type": challenge_type,
        "recommendation": recommendation,
        "confidence_level": confidence,
        "notes": description
    }
    
    if risks:
        challenge["risk_assessment"] = {
            "risk_level": "high" if len(risks) > 2 else "medium" if len(risks) > 0 else "low",
            "risks": risks
        }
    
    if alternative:
        challenge["alternative_approach"] = alternative
    
    if impact:
        challenge["impact_analysis"] = impact
    
    if reasoning:
        challenge["first_principles_reasoning"] = reasoning
    
    # Validate against schema
    schema_path = os.path.join(os.path.dirname(__file__), '../../knowledge-base/protocols/challenge_schema.json')
    try:
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                schema = json.load(f)
            # Basic validation - check required fields
            required = schema.get('required', [])
            for field in required:
                if field not in challenge:
                    logger.log(f"Missing required field: {field}", "WARNING")
    except Exception as e:
        logger.log(f"Schema validation error: {e}", "WARNING")
    
    # Save challenge
    os.makedirs('.tmp', exist_ok=True)
    challenge_file = f'.tmp/challenge_{challenge_id}.json'
    with open(challenge_file, 'w') as f:
        json.dump(challenge, f, indent=2)
    
    # Log to central log
    logger.log(f"Challenge submitted: {challenge_type} for proposal {proposal_id}")
    
    return challenge

def main():
    parser = argparse.ArgumentParser(description='Propose improvement or challenge')
    parser.add_argument('--proposal-id', required=True, help='Proposal being challenged')
    parser.add_argument('--department', required=True, help='Your department')
    parser.add_argument('--type', required=True, choices=['risk_identified', 'better_alternative', 'optimization', 'feasibility_concern', 'question'])
    parser.add_argument('--description', required=True, help='Description of challenge/improvement')
    parser.add_argument('--risks', nargs='+', help='List of risks')
    parser.add_argument('--recommendation', default='approve_with_changes', choices=['approve_as_is', 'approve_with_changes', 'need_more_info', 'reject'])
    parser.add_argument('--confidence', default='high', choices=['very_high', 'high', 'medium', 'low'])
    
    args = parser.parse_args()
    
    result = propose_improvement(
        proposal_id=args.proposal_id,
        department=args.department,
        challenge_type=args.type,
        description=args.description,
        risks=args.risks,
        recommendation=args.recommendation,
        confidence=args.confidence
    )
    
    print("\n=== Challenge Submitted ===")
    print(json.dumps(result, indent=2))
    print(f"\nChallenge ID: {result['challenge_id']}")

if __name__ == "__main__":
    main()
