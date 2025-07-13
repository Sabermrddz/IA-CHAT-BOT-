#!/usr/bin/env python3
"""
Test script for the updated chat API with OpenRouter
"""
import requests
import json

def test_chat_api():
    """Test the updated chat API with OpenRouter"""
    base_url = "http://localhost:8000/chat-ai/"
    headers = {"Content-Type": "application/json"}
    
    print("Testing updated chat API with OpenRouter (tencent/hunyuan-a13b-instruct:free)...")
    print("=" * 50)
    
    # Test 1: First message (new chat)
    print("\n1. First message (new chat):")
    data1 = {
        "message": "I have a headache",
        "conversation_history": [],
        "is_new_chat": True
    }
    
    try:
        response1 = requests.post(base_url, headers=headers, json=data1, timeout=30)
        print(f"Status: {response1.status_code}")
        
        if response1.status_code == 200:
            result1 = response1.json()
            print(f"✅ Success! AI Response: {result1['response'][:100]}...")
            
            # Test 2: Follow-up message with conversation history
            print("\n2. Follow-up message (with conversation history):")
            data2 = {
                "message": "What should I do about it?",
                "conversation_history": [
                    {"role": "user", "content": "I have a headache"},
                    {"role": "assistant", "content": result1['response']}
                ],
                "is_new_chat": False
            }
            
            response2 = requests.post(base_url, headers=headers, json=data2, timeout=30)
            print(f"Status: {response2.status_code}")
            
            if response2.status_code == 200:
                result2 = response2.json()
                print(f"✅ Success! AI Response: {result2['response'][:100]}...")
                
                # Test 3: Non-medical question (should be rejected)
                print("\n3. Non-medical question test:")
                data3 = {
                    "message": "What's the weather like today?",
                    "conversation_history": [],
                    "is_new_chat": False
                }
                
                response3 = requests.post(base_url, headers=headers, json=data3, timeout=30)
                print(f"Status: {response3.status_code}")
                
                if response3.status_code == 200:
                    result3 = response3.json()
                    print(f"AI Response: {result3['response'][:100]}...")
                else:
                    print(f"❌ Error: {response3.text}")
                    
            else:
                print(f"❌ Error: {response2.text}")
                
        else:
            print(f"❌ Error: {response1.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: Request took too long")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_chat_api() 