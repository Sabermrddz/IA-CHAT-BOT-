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

    logger = logging.getLogger(__name__)

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
            """

            try:
                # Log email settings
                logger.info(f"Using email backend: {settings.EMAIL_BACKEND}")
                logger.info(f"Sending from: {settings.EMAIL_HOST_USER}")
                logger.info(f"Using SMTP server: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")

                # Send email
                send_mail(
                    subject=f"Contact Form: {subject}",
                    message=full_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )

                return JsonResponse({
                    'success': True,
                    'message': 'Your message has been sent successfully!'
                })

            except BadHeaderError:
                logger.error("BadHeaderError in email sending")
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid header found in the message.'
                })
            except Exception as e:
                logger.error(f"Email sending failed: {str(e)}")
                logger.error(traceback.format_exc())
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to send email. Please try again later.'
                })

        except Exception as e:
            logger.error(f"Form processing error: {str(e)}")
            logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'error': 'An unexpected error occurred. Please try again.'
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