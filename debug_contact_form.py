#!/usr/bin/env python3
"""
Debug script for contact form issues
"""

import requests
import json
import sys

def test_endpoints(base_url):
    """Test various endpoints to identify issues"""
    
    print("=== Contact Form Debug Test ===")
    print(f"Testing base URL: {base_url}")
    
    # Test 1: Health endpoint
    print("\n1. Testing health endpoint...")
    try:
        health_response = requests.get(f"{base_url}/health/")
        print(f"   Status: {health_response.status_code}")
        if health_response.ok:
            health_data = health_response.json()
            print(f"   Response: {json.dumps(health_data, indent=2)}")
        else:
            print(f"   Error: {health_response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Test contact endpoint
    print("\n2. Testing contact endpoint...")
    try:
        test_data = {"test": "data"}
        test_response = requests.post(
            f"{base_url}/test-contact/",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"   Status: {test_response.status_code}")
        if test_response.ok:
            test_data = test_response.json()
            print(f"   Response: {json.dumps(test_data, indent=2)}")
        else:
            print(f"   Error: {test_response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Contact page (GET)
    print("\n3. Testing contact page...")
    try:
        contact_response = requests.get(f"{base_url}/contact")
        print(f"   Status: {contact_response.status_code}")
        if contact_response.ok:
            print(f"   Content length: {len(contact_response.text)}")
            if "contactForm" in contact_response.text:
                print("   ✓ Contact form found in HTML")
            else:
                print("   ✗ Contact form not found in HTML")
        else:
            print(f"   Error: {contact_response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: CSRF token
    print("\n4. Testing CSRF token...")
    try:
        csrf_response = requests.get(f"{base_url}/contact")
        if csrf_response.ok:
            if "csrfmiddlewaretoken" in csrf_response.text:
                print("   ✓ CSRF token found in HTML")
            else:
                print("   ✗ CSRF token not found in HTML")
        else:
            print(f"   Error: {csrf_response.text}")
    except Exception as e:
        print(f"   Error: {e}")

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"
    
    test_endpoints(base_url)

if __name__ == "__main__":
    main() 