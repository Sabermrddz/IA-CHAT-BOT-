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
    from django.core.mail import send_mail
    from django.conf import settings
    from django.http import JsonResponse
    import json
    import re

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', 'General Inquiry')
        message = request.POST.get('message', '')

        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return JsonResponse({'success': False, 'error': 'Invalid email format'})

        # Validate name (only letters, spaces, and hyphens)
        name_regex = r'^[a-zA-Z\s-]+$'
        if not re.match(name_regex, name):
            return JsonResponse({'success': False, 'error': 'Invalid name format'})

        try:
            full_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nSubject: {subject}\nMessage: {message}"
            send_mail(
                subject=f"Contact Form: {subject}",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return render(request, 'clinic/contact.html', {'success': True})
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            return render(request, 'clinic/contact.html', {'error': str(e)})

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