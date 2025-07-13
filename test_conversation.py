#!/usr/bin/env python3
"""
Test script for conversation history functionality
"""
import requests
import json

def test_conversation_history():
    """Test conversation history functionality"""
    base_url = "http://localhost:8000/chat-ai/"
    headers = {"Content-Type": "application/json"}
    
    print("Testing conversation history...")
    
    # Test 1: First message (new chat)
    print("\n1. First message (new chat):")
    data1 = {
        "message": "I have a headache",
        "conversation_history": [],
        "is_new_chat": True
    }
    
    response1 = requests.post(base_url, headers=headers, json=data1)
    print(f"Status: {response1.status_code}")
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"Response: {result1['response'][:100]}...")
        
        # Extract the assistant's response for history
        assistant_response = result1['response'].split('\n\n', 1)[-1] if '\n\n' in result1['response'] else result1['response']
        
        # Test 2: Follow-up message with history
        print("\n2. Follow-up message (with history):")
        data2 = {
            "message": "What should I do about it?",
            "conversation_history": [
                {"role": "user", "content": "I have a headache"},
                {"role": "assistant", "content": assistant_response}
            ],
            "is_new_chat": False
        }
        
        response2 = requests.post(base_url, headers=headers, json=data2)
        print(f"Status: {response2.status_code}")
        if response2.status_code == 200:
            result2 = response2.json()
            print(f"Response: {result2['response']}")
        else:
            print(f"Error: {response2.text}")
    else:
        print(f"Error: {response1.text}")

if __name__ == "__main__":
    test_conversation_history() 