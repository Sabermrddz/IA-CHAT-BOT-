#!/usr/bin/env python3
"""
Test script for the new frontend-backend chat integration
"""
import requests
import json

def test_new_chat_integration():
    """Test the new chat integration with system instructions and conversation history"""
    base_url = "http://localhost:8000/chat-ai/"
    headers = {"Content-Type": "application/json"}
    
    print("Testing new chat integration...")
    
    # Test 1: First message with system instruction
    print("\n1. First message (with system instruction):")
    data1 = {
        "message": "I have a headache",
        "conversation_history": [],
        "is_new_chat": False,
        "messages": [
            {
                "role": "system",
                "content": "You are Inspair.Health, a concise multilingual AI medical assistant. You only answer in the language the user uses. Never talk about non-medical topics. Always reply briefly and clearly."
            },
            {
                "role": "user",
                "content": "I have a headache"
            }
        ]
    }
    
    response1 = requests.post(base_url, headers=headers, json=data1)
    print(f"Status: {response1.status_code}")
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"Response: {result1['response']}")
        
        # Test 2: Follow-up message with full conversation history
        print("\n2. Follow-up message (with full conversation history):")
        data2 = {
            "message": "What should I do about it?",
            "conversation_history": [
                {"role": "user", "content": "I have a headache"},
                {"role": "assistant", "content": result1['response']}
            ],
            "is_new_chat": False,
            "messages": [
                {
                    "role": "system",
                    "content": "You are Inspair.Health, a concise multilingual AI medical assistant. You only answer in the language the user uses. Never talk about non-medical topics. Always reply briefly and clearly."
                },
                {"role": "user", "content": "I have a headache"},
                {"role": "assistant", "content": result1['response']},
                {"role": "user", "content": "What should I do about it?"}
            ]
        }
        
        response2 = requests.post(base_url, headers=headers, json=data2)
        print(f"Status: {response2.status_code}")
        if response2.status_code == 200:
            result2 = response2.json()
            print(f"Response: {result2['response']}")
            
            # Test 3: Multilingual test
            print("\n3. Multilingual test (Spanish):")
            data3 = {
                "message": "Tengo dolor de cabeza",
                "conversation_history": [],
                "is_new_chat": False,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Inspair.Health, a concise multilingual AI medical assistant. You only answer in the language the user uses. Never talk about non-medical topics. Always reply briefly and clearly."
                    },
                    {"role": "user", "content": "Tengo dolor de cabeza"}
                ]
            }
            
            response3 = requests.post(base_url, headers=headers, json=data3)
            print(f"Status: {response3.status_code}")
            if response3.status_code == 200:
                result3 = response3.json()
                print(f"Response: {result3['response']}")
            else:
                print(f"Error: {response3.text}")
        else:
            print(f"Error: {response2.text}")
    else:
        print(f"Error: {response1.text}")

if __name__ == "__main__":
    test_new_chat_integration() 