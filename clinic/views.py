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

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', 'General Inquiry').strip()
        message = request.POST.get('message', '').strip()

        # Validation
        if not all([name, email, message]):
            return JsonResponse({
                'success': False,
                'error': 'Please fill in all required fields.'
            })

        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return JsonResponse({
                'success': False,
                'error': 'Please enter a valid email address.'
            })

        # Validate name (only letters, spaces, and hyphens)
        name_regex = r'^[a-zA-Z\s-]+$'
        if not re.match(name_regex, name):
            return JsonResponse({
                'success': False,
                'error': 'Name should only contain letters, spaces, and hyphens.'
            })

        try:
            # Construct email message
            full_message = (
                f"New Contact Form Submission\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Subject: {subject}\n\n"
                f"Message:\n{message}"
            )

            # Send email
            send_mail(
                subject=f"Contact Form: {subject}",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            
            return JsonResponse({'success': True})
            
        except BadHeaderError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid header found in the message.'
            })
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'There was an error sending your message. Please try again later.'
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