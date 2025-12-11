"""
Debug test to capture exact request/response for issue #13.

This test helps diagnose why the API is still returning error 11
even after the SDK fix.
"""

import os
import json
import requests
from cloze_sdk import ClozeClient
from cloze_sdk.exceptions import ClozeAPIError


def test_debug_request():
    """Capture exact request/response to debug error 11."""
    api_key = os.getenv("CLOZE_API_KEY")
    if not api_key:
        # Try to read from file
        key_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "tmp", "api_key.txt")
        if os.path.exists(key_file):
            with open(key_file, "r") as f:
                api_key = f.read().strip()
    
    if not api_key:
        print("No API key found")
        return
    
    client = ClozeClient(api_key=api_key)
    
    # Test data from user's contact list
    test_cases = [
        {
            "name": "Rhea Bhatia",
            "email": "rheabhatia@rocketmail.com",
            "first": "Rhea",
            "last": "Bhatia"
        },
        {
            "name": "Stephanie Koogler",
            "email": "skoogler@deezee.com",
            "first": "Stephanie",
            "last": "Koogler"
        }
    ]
    
    for person_data in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {person_data['name']} ({person_data['email']})")
        print(f"{'='*60}")
        
        # Test 1: Using SDK (wrapped format)
        print("\n[TEST 1] Using SDK (wrapped format)")
        try:
            result = client.people.create(person_data)
            print(f"SUCCESS: {json.dumps(result, indent=2)}")
        except ClozeAPIError as e:
            print(f"ERROR: {e}")
            print(f"Error code: {e.errorcode if hasattr(e, 'errorcode') else 'unknown'}")
            if hasattr(e, 'response') and e.response:
                print(f"Response status: {e.response.status_code}")
                try:
                    print(f"Response body: {json.dumps(e.response.json(), indent=2)}")
                except:
                    print(f"Response text: {e.response.text}")
        
        # Test 2: Direct API call with wrapped format
        print("\n[TEST 2] Direct API call (wrapped format)")
        try:
            response = requests.post(
                "https://api.cloze.com/v1/people/create",
                json={"person": person_data},
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Exception: {e}")
        
        # Test 3: Direct API call without wrapping
        print("\n[TEST 3] Direct API call (no wrapping)")
        try:
            response = requests.post(
                "https://api.cloze.com/v1/people/create",
                json=person_data,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Exception: {e}")


if __name__ == "__main__":
    test_debug_request()

