from django.shortcuts import render
from .daily_posts_views import live_posts_api
from .chat_views import chat_ai

# Create your views here.

def home(request):
    """Homepage view for the medical clinic website."""
    return render(request, 'clinic/home.html')

def about(request):
    """About page view for the medical clinic."""
    return render(request, 'clinic/about.html')

def contact(request):
    """Contact page view for the medical clinic."""
    from django.core.mail import send_mail, BadHeaderError
    from django.conf import settings
    from django.http import JsonResponse
    import re
    import traceback
    import logging
    import os
    import json

    logger = logging.getLogger(__name__)
    
    # Log request information for debugging
    logger.info(f"Contact form request: {request.method}")
    if request.method == 'POST':
        logger.info(f"Request headers: {dict(request.headers)}")
        logger.info(f"Request content type: {request.content_type}")

    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            subject = request.POST.get('subject', 'General Inquiry').strip()
            message = request.POST.get('message', '').strip()

            # Basic validation
            if not all([name, email, message]):
                return JsonResponse({
                    'success': False,
                    'error': 'Please fill in all required fields (Name, Email, and Message).'
                })

            # Email format validation
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                return JsonResponse({
                    'success': False,
                    'error': 'Please enter a valid email address.'
                })

            # Construct email message
            full_message = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message}

---
Sent from Inspair.Health Contact Form
            """

            # Check if email settings are properly configured
            email_host_user = os.getenv('EMAIL_HOST_USER')
            email_host_password = os.getenv('EMAIL_HOST_PASSWORD')
            
            if not email_host_user or not email_host_password:
                logger.error("Email credentials not configured")
                return JsonResponse({
                    'success': False,
                    'error': 'Email service is not configured. Please contact the administrator.'
                })

            try:
                # Log email settings (without sensitive data)
                logger.info(f"Using email backend: {settings.EMAIL_BACKEND}")
                logger.info(f"Email host: {settings.EMAIL_HOST}")
                logger.info(f"Email port: {settings.EMAIL_PORT}")
                logger.info(f"Email TLS: {settings.EMAIL_USE_TLS}")
                logger.info(f"Email user configured: {'Yes' if email_host_user else 'No'}")

                # Send email
                send_mail(
                    subject=f"Contact Form: {subject}",
                    message=full_message,
                    from_email=email_host_user,
                    recipient_list=[email_host_user],  # Send to the same email
                    fail_silently=False,
                )

                logger.info("Email sent successfully")
                return JsonResponse({
                    'success': True,
                    'message': 'Your message has been sent successfully! We will get back to you within 24 hours.'
                })

            except BadHeaderError as e:
                logger.error(f"BadHeaderError in email sending: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid header found in the message. Please check your input and try again.'
                })
            except Exception as e:
                logger.error(f"Email sending failed: {str(e)}")
                logger.error(traceback.format_exc())
                
                # Provide more specific error messages
                if "Authentication" in str(e):
                    return JsonResponse({
                        'success': False,
                        'error': 'Email authentication failed. Please contact the administrator.'
                    })
                elif "Connection" in str(e):
                    return JsonResponse({
                        'success': False,
                        'error': 'Unable to connect to email server. Please try again later.'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Failed to send email. Please try again later or contact us directly.'
                    })

        except Exception as e:
            logger.error(f"Form processing error: {str(e)}")
            logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'error': 'An unexpected error occurred. Please try again or contact us directly.'
            })

    return render(request, 'clinic/contact.html')

def daily_posts(request):
    """Daily posts page view for the medical clinic."""
    return render(request, 'clinic/daily_posts.html')

def chat_box(request):
    """Chat box page view for the medical clinic."""
    return render(request, 'clinic/chat_box.html')


def how_it_woks(request):
    """Chat box page view for the medical clinic."""
    return render(request, 'clinic/how_it_woks.html')

def health_check(request):
    """Health check endpoint for Railway deployment."""
    from django.http import JsonResponse
    import os
    
    # Check environment variables
    email_user = os.getenv('EMAIL_HOST_USER')
    email_password = os.getenv('EMAIL_HOST_PASSWORD')
    debug_mode = os.getenv('DEBUG', 'False')
    
    health_status = {
        'status': 'healthy',
        'email_configured': bool(email_user and email_password),
        'debug_mode': debug_mode == 'True',
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'email_backend': settings.EMAIL_BACKEND,
        'email_host': settings.EMAIL_HOST,
        'email_port': settings.EMAIL_PORT,
        'email_use_tls': settings.EMAIL_USE_TLS,
        'request_method': request.method,
        'request_path': request.path,
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
    }
    
    return JsonResponse(health_status)

def test_contact(request):
    """Test endpoint for contact form debugging."""
    from django.http import JsonResponse
    
    if request.method == 'POST':
        # Log the request details
        logger = logging.getLogger(__name__)
        logger.info(f"Test contact POST request received")
        logger.info(f"Request headers: {dict(request.headers)}")
        logger.info(f"Request content type: {request.content_type}")
        logger.info(f"Request body: {request.body}")
        
        return JsonResponse({
            'success': True,
            'message': 'Test contact endpoint working',
            'received_data': dict(request.POST) if request.POST else 'No POST data'
        })
    
    return JsonResponse({
        'success': False,
        'message': 'This endpoint only accepts POST requests'
    })