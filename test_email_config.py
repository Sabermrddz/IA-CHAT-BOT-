#!/usr/bin/env python3
"""
Test script to verify email configuration on Railway
Run this script to test if email settings are properly configured
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_email_config():
    """Test email configuration"""
    print("=== Email Configuration Test ===")
    
    # Check environment variables
    email_user = os.getenv('EMAIL_HOST_USER')
    email_password = os.getenv('EMAIL_HOST_PASSWORD')
    
    print(f"EMAIL_HOST_USER: {'✓ Set' if email_user else '✗ Not set'}")
    print(f"EMAIL_HOST_PASSWORD: {'✓ Set' if email_password else '✗ Not set'}")
    
    # Check Django settings
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    if not email_user or not email_password:
        print("\n❌ Email credentials are not properly configured!")
        print("Please set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD environment variables.")
        return False
    
    # Test email sending
    print("\n=== Testing Email Sending ===")
    try:
        test_message = """
This is a test email from Inspair.Health

If you receive this email, the email configuration is working properly.

---
Test sent from Railway deployment
        """
        
        send_mail(
            subject="Test Email - Inspair.Health",
            message=test_message,
            from_email=email_user,
            recipient_list=[email_user],
            fail_silently=False,
        )
        
        print("✅ Test email sent successfully!")
        print("Check your email inbox for the test message.")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {str(e)}")
        print("\nCommon issues:")
        print("1. Gmail App Password not set correctly")
        print("2. 2FA not enabled on Gmail account")
        print("3. Less secure app access not enabled")
        print("4. Network connectivity issues")
        return False

if __name__ == "__main__":
    success = test_email_config()
    sys.exit(0 if success else 1) 