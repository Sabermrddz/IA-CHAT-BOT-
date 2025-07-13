import os
import requests
import random
import logging
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from langdetect import detect, DetectorFactory

# Set seed for consistent language detection
DetectorFactory.seed = 0


def is_english_text(text):
    """
    Check if the given text is in English.
    Uses multiple methods for better accuracy.
    """
    if not text or not isinstance(text, str):
        return False
    
    # Remove HTML tags and clean text
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = text.strip()
    
    if len(text) < 10:  # Too short to reliably detect
        return False
    
    # Check for Arabic characters (common non-English content)
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
    if arabic_pattern.search(text):
        return False
    
    # Check for other non-Latin scripts
    non_latin_pattern = re.compile(r'[\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7AF\u0E00-\u0E7F\u0E80-\u0EFF\u0F00-\u0FFF\u1000-\u109F\u1100-\u11FF\u1200-\u137F\u1380-\u139F\u13A0-\u13FF\u1400-\u167F\u1680-\u169F\u16A0-\u16FF\u1700-\u171F\u1720-\u173F\u1740-\u175F\u1760-\u177F\u1780-\u17FF\u1800-\u18AF\u1900-\u194F\u1950-\u197F\u1980-\u19DF\u19E0-\u19FF\u1A00-\u1A1F\u1A20-\u1AAF\u1AB0-\u1AFF\u1B00-\u1B7F\u1B80-\u1BBF\u1BC0-\u1BFF\u1C00-\u1C4F\u1C50-\u1C7F\u1C80-\u1C8F\u1C90-\u1CBF\u1CC0-\u1CCF\u1CD0-\u1CFF\u1D00-\u1D7F\u1D80-\u1DBF\u1DC0-\u1DFF\u1E00-\u1EFF\u1F00-\u1FFF\u2000-\u206F\u2070-\u209F\u20A0-\u20CF\u20D0-\u20FF\u2100-\u214F\u2150-\u218F\u2190-\u21FF\u2200-\u22FF\u2300-\u23FF\u2400-\u243F\u2440-\u245F\u2460-\u24FF\u2500-\u257F\u2580-\u259F\u25A0-\u25FF\u2600-\u26FF\u2700-\u27BF\u27C0-\u27EF\u27F0-\u27FF\u2800-\u28FF\u2900-\u297F\u2980-\u29FF\u2A00-\u2AFF\u2B00-\u2BFF\u2C00-\u2C5F\u2C60-\u2C7F\u2C80-\u2CFF\u2D00-\u2D2F\u2D30-\u2D7F\u2D80-\u2DDF\u2DE0-\u2DFF\u2E00-\u2E7F\u2E80-\u2EFF\u2F00-\u2FDF\u2FF0-\u2FFF\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\u3100-\u312F\u3130-\u318F\u3190-\u319F\u31A0-\u31BF\u31C0-\u31EF\u31F0-\u31FF\u3200-\u32FF\u3300-\u33FF\u3400-\u4DBF\u4DC0-\u4DFF\u4E00-\u9FFF\uA000-\uA48F\uA490-\uA4CF\uA4D0-\uA4FF\uA500-\uA63F\uA640-\uA69F\uA6A0-\uA6FF\uA700-\uA71F\uA720-\uA7FF\uA800-\uA82F\uA830-\uA83F\uA840-\uA87F\uA880-\uA8DF\uA8E0-\uA8FF\uA900-\uA92F\uA930-\uA95F\uA960-\uA97F\uA980-\uA9DF\uA9E0-\uA9FF\uAA00-\uAA5F\uAA60-\uAA7F\uAA80-\uAADF\uAAE0-\uAAFF\uAB00-\uAB2F\uAB30-\uAB6F\uAB70-\uABBF\uABC0-\uABFF\uAC00-\uD7AF\uD7B0-\uD7FF\uD800-\uDB7F\uDB80-\uDBFF\uDC00-\uDFFF\uE000-\uF8FF\uF900-\uFAFF\uFB00-\uFB4F\uFB50-\uFDFF\uFE00-\uFE0F\uFE10-\uFE1F\uFE20-\uFE2F\uFE30-\uFE4F\uFE50-\uFE6F\uFE70-\uFEFF\uFF00-\uFFEF\uFFF0-\uFFFF]')
    if non_latin_pattern.search(text):
        return False
    
    try:
        # Use langdetect to detect language
        detected_lang = detect(text)
        return detected_lang == 'en'
    except:
        # Fallback: check for common English patterns
        english_pattern = re.compile(r'^[a-zA-Z\s\.,!?;:\'\"()-]+$')
        return bool(english_pattern.match(text))


def filter_english_articles(articles):
    """
    Filter articles to only include those with English titles and descriptions.
    """
    english_articles = []
    
    for article in articles:
        title = article.get('title', '')
        description = article.get('description', '')
        
        # Check if both title and description are in English
        if is_english_text(title) and is_english_text(description):
            english_articles.append(article)
        else:
            logging.info(f"Filtered out non-English article: {title[:50]}...")
    
    return english_articles


@csrf_exempt
@require_http_methods(["POST"])
def live_posts_api(request):
    """API endpoint for fetching live health news posts."""
    logging.info("=== LIVE POSTS API CALLED ===")
    logging.info(f"Request method: {request.method}")
    logging.info(f"Request headers: {dict(request.headers)}")
    
    NEWSAPI_URL = "https://newsapi.org/v2/everything"
    
    # Get API key from environment variables
    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        logging.error("NewsAPI key not found in environment variables")
        return JsonResponse({
            'articles': [],
            'status': 'error',
            'newsapi_message': 'API configuration error: NEWSAPI_KEY not set.'
        }, status=500)
    
    # Randomize the page number for each request
    page = random.randint(1, 5)
    params = {
        'q': 'health OR medicine OR disease',
        'language': 'en',
        'apiKey': api_key,
        'page': page,
        'pageSize': 20,
    }
    
    try:
        r = requests.get(NEWSAPI_URL, params=params, timeout=10)
        logging.info(f"NewsAPI request URL: {r.url}")
        r.raise_for_status()  # Raise an exception for bad status codes
        data = r.json()
        logging.info(f"NewsAPI raw response: {data}")
        
        # Handle API errors
        if data.get('status') != 'ok':
            logging.error(f"NewsAPI error: {data.get('message')}")
            return JsonResponse({
                'articles': [],
                'status': data.get('status', 'error'),
                'newsapi_message': data.get('message', 'Live news unavailable. Please try later.'),
                'newsapi_raw': data
            }, status=200)
        
        # Get all articles from the response
        all_articles = data.get('articles', [])
        logging.info(f"Received {len(all_articles)} articles from NewsAPI")
        
        # TEMPORARILY: Skip filtering and return all articles
        # english_articles = filter_english_articles(all_articles)
        english_articles = all_articles  # Return all articles without filtering
        logging.info(f"Returning {len(english_articles)} articles (filtering disabled)")
        
        return JsonResponse({
            'articles': english_articles,
            'status': data.get('status'),
            'newsapi_message': data.get('message', ''),
            'total_received': len(all_articles),
            'english_filtered': len(english_articles),
            'newsapi_raw': data
        })
        
    except requests.exceptions.RequestException as e:
        logging.error(f"NewsAPI fetch error: {e}")
        return JsonResponse({
            'articles': [],
            'error': 'Failed to fetch news',
            'status': 'error',
            'newsapi_message': str(e)
        }, status=500)
    except Exception as e:
        logging.error(f"Unexpected error in live_posts_api: {e}")
        return JsonResponse({
            'articles': [],
            'error': 'Internal server error',
            'status': 'error',
            'newsapi_message': str(e)
        }, status=500) 