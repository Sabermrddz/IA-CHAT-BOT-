import os
import requests
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

@csrf_exempt
@require_http_methods(["POST"])
def chat_ai(request):
    """AI chat endpoint for medical assistance."""
    try:
        # Parse request data
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            logging.error(f"[chat_ai] Invalid JSON: {e}")
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        message = data.get('message', '').strip()
        conversation_history = data.get('conversation_history', [])
        is_new_chat = data.get('is_new_chat', False)

        if not message:
            return JsonResponse({'error': 'No message provided'}, status=400)
        if not isinstance(conversation_history, list):
            conversation_history = []
        MAX_HISTORY = 10
        if len(conversation_history) > MAX_HISTORY:
            conversation_history = conversation_history[-MAX_HISTORY:]

        # OpenRouter API config
        import os
        api_key = os.getenv('OPENROUTER_API_KEY')
        endpoint = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Inspair.Health"
        }

        # System prompt
        system_prompt = (
            "You are a professional medical AI assistant for Inspair.Health, developed by Mourad Mostafa Saber. Your ONLY purpose is to provide medical information and health guidance.\n\n"
            "STRICT RULES - YOU MUST FOLLOW THESE:\n"
            "1. ONLY answer questions about: medical conditions, symptoms, treatments, medications, health advice, nutrition, exercise for health, mental health, preventive care, and general health information\n"
            "2. If asked about ANY non-health topic (technology, sports, news, entertainment, politics, etc.), respond with: 'I am a medical AI assistant and can only help with health-related questions. Please ask me about medical topics, symptoms, treatments, or general health information.'\n"
            "3. Always provide clear, concise, and professional medical information\n"
            "4. Use simple, understandable language while maintaining medical accuracy\n"
            "5. Always include this disclaimer: 'This is for informational purposes only. Please consult a healthcare professional for medical advice.'\n"
            "6. Never provide definitive diagnoses - only general information and guidance\n"
            "7. If unsure about a medical topic, say: 'I recommend consulting with a healthcare professional for this specific medical question.'\n"
            "8. Keep responses focused and to the point\n"
            "9. Respond in the same language as the user (English or Arabic)\n\n"
            "EXAMPLE RESPONSES:\n"
            "- For non-health questions: 'I am a medical AI assistant and can only help with health-related questions. Please ask me about medical topics, symptoms, treatments, or general health information.'\n"
            "- For health questions: Provide clear, professional medical information with the disclaimer\n\n"
            "CRITICAL: Respond with plain text only. No XML tags, HTML tags, or special formatting. Write your response directly."
        )

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (limit to last 6 exchanges to prevent token overflow)
        history_limit = 12  # 6 user + 6 assistant messages
        recent_history = conversation_history[-history_limit:] if len(conversation_history) > history_limit else conversation_history
        
        for msg in recent_history:
            if (
                isinstance(msg, dict)
                and msg.get('role') in ['user', 'assistant']
                and isinstance(msg.get('content'), str)
                and msg.get('content').strip()
            ):
                # Clean any XML tags from history too
                content = msg['content'].strip()
                import re
                content = re.sub(r'<[^>]+>', '', content)  # Remove any XML tags
                content = re.sub(r'\s+', ' ', content).strip()  # Clean whitespace
                
                if content:  # Only add if content is not empty after cleaning
                    messages.append({
                        "role": msg['role'],
                        "content": content[:300]  # Shorter limit for history
                    })
        
        logging.info(f"[chat_ai] Built {len(messages)} messages for API call")
        logging.info(f"[chat_ai] Conversation history length: {len(recent_history)}")
        # Add language context to help the AI understand what language to respond in
        language_context = ""
        if any(char.isascii() and char.isalpha() for char in message):
            # Contains English letters
            language_context = " (Please respond in English)"
        elif any('\u0600' <= char <= '\u06ff' for char in message):
            # Contains Arabic characters
            language_context = " (يرجى الرد باللغة العربية)"
        
        messages.append({"role": "user", "content": message + language_context})

        payload = {
            "model": "tencent/hunyuan-a13b-instruct:free",
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.7,
            "stream": False
        }

        logging.info(f"[chat_ai] Sending to OpenRouter: {json.dumps(payload)}")
        
        # Retry mechanism for temporary availability issues
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                r = requests.post(endpoint, headers=headers, json=payload, timeout=30)
                logging.info(f"[chat_ai] OpenRouter status: {r.status_code}")
                logging.info(f"[chat_ai] OpenRouter response: {r.text}")
                
                # If successful, break out of retry loop
                if r.status_code == 200:
                    break
                    
                # If 503 and not the last attempt, wait and retry
                if r.status_code == 503 and attempt < max_retries:
                    logging.info(f"[chat_ai] 503 error, retrying in 2 seconds... (attempt {attempt + 1}/{max_retries + 1})")
                    import time
                    time.sleep(2)
                    continue
                    
            except Exception as e:
                logging.error(f"[chat_ai] Network error: {e}")
                if attempt == max_retries:
                    return JsonResponse({'error': 'Network error contacting AI service', 'details': str(e)}, status=502)
                continue

        if r.status_code != 200:
            # Handle specific OpenRouter errors
            if r.status_code == 503:
                try:
                    error_data = r.json()
                    if "No instances available" in r.text:
                        return JsonResponse({
                            'error': 'AI service temporarily unavailable',
                            'details': 'The free AI model is currently busy. Please try again in a few minutes.'
                        }, status=503)
                except:
                    pass
            return JsonResponse({'error': f'OpenRouter API error: {r.status_code}', 'details': r.text}, status=502)

        try:
            resp_data = r.json()
        except Exception as e:
            logging.error(f"[chat_ai] Invalid JSON from OpenRouter: {e}")
            return JsonResponse({'error': 'Invalid response from AI service', 'details': r.text}, status=502)

        # Extract AI response
        choices = resp_data.get('choices')
        logging.info(f"[chat_ai] Full response data: {json.dumps(resp_data, indent=2)}")
        
        if not choices or not isinstance(choices, list):
            logging.error(f"[chat_ai] No choices in response: {resp_data}")
            return JsonResponse({'error': 'No response choices from AI service', 'details': resp_data}, status=502)
            
        if not choices[0].get('message'):
            logging.error(f"[chat_ai] No message in first choice: {choices[0]}")
            return JsonResponse({'error': 'No message in AI response', 'details': choices[0]}, status=502)
            
        logging.info(f"[chat_ai] Raw AI message: {choices[0]['message']}")
        ai_message = choices[0]['message'].get('content', '').strip()
        
        # Clean up XML tags and formatting
        import re
        # Remove <answer> and </answer> tags
        ai_message = re.sub(r'<answer>\s*', '', ai_message)
        ai_message = re.sub(r'\s*</answer>', '', ai_message)
        # Remove any other XML-like tags
        ai_message = re.sub(r'<[^>]+>', '', ai_message)
        # Clean up extra whitespace
        ai_message = re.sub(r'\s+', ' ', ai_message).strip()
        
        if not ai_message:
            logging.warning("[chat_ai] Empty response after cleaning, using fallback")
            # Try to get the original content before cleaning
            original_content = choices[0]['message'].get('content', '')
            if original_content and original_content.strip():
                ai_message = original_content.strip()
            else:
                ai_message = "I'm sorry, I couldn't generate a response. Please try again."
            
        logging.info(f"[chat_ai] Final cleaned response: {ai_message}")
        return JsonResponse({'response': ai_message})

    except Exception as e:
        logging.error(f"[chat_ai] Server error: {e}")
        return JsonResponse({'error': 'Internal server error', 'details': str(e)}, status=500) 