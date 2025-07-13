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
    from django.contrib import messages

    context = {}
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', 'General Inquiry')
        message = request.POST.get('message', '')

        try:
            full_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nSubject: {subject}\nMessage: {message}"
            send_mail(
                subject=f"Contact Form: {subject}",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            context['success'] = True
            messages.success(request, "Thank you! Your message has been sent successfully.")
        except Exception as e:
            messages.error(request, "Sorry, there was an error sending your message. Please try again later.")
            print(f"Error sending email: {str(e)}")
            
    return render(request, 'clinic/contact.html', context)

def daily_posts(request):
    """Daily posts page view for the medical clinic."""
    return render(request, 'clinic/daily_posts.html')

def chat_box(request):
    """Chat box page view for the medical clinic."""
    return render(request, 'clinic/chat_box.html')


def how_it_woks(request):
    """Chat box page view for the medical clinic."""
    return render(request, 'clinic/how_it_woks.html')