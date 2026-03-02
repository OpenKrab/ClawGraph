#!/usr/bin/env python3
"""
ClawGraph Improve Script
Sends feedback to ClawSelfImprove for learning
"""

import sys
import requests
import yaml
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent.parent / 'config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def send_feedback_to_claw_self_improve(feedback, config):
    """
    Send feedback to ClawSelfImprove API
    This is a placeholder - adjust based on actual ClawSelfImprove API
    """
    # Assume ClawSelfImprove has an API endpoint
    # For now, just log the feedback
    print(f"Sending feedback to ClawSelfImprove: {feedback}")

    # TODO: Implement actual API call
    # api_url = config.get('claw_self_improve', {}).get('api_url', 'http://localhost:3000/api/improve')
    # response = requests.post(api_url, json={'feedback': feedback, 'source': 'claw-graph'})
    # return response.json()

    return {"status": "logged", "feedback": feedback}

def main():
    if len(sys.argv) < 2:
        print("Usage: python improve.py 'feedback text'")
        return 1

    feedback = sys.argv[1]

    try:
        config = load_config()
        result = send_feedback_to_claw_self_improve(feedback, config)

        print("Feedback sent:")
        print(result)

    except Exception as e:
        print(f"Error sending feedback: {e}")
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
