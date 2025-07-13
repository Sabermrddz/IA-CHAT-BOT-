from django.urls import path
from . import views

app_name = 'clinic'

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('daily_posts', views.daily_posts, name='daily_posts'),
    path('chat_box', views.chat_box, name='chat_box'),
    path('how_it_woks', views.how_it_woks, name='how_it_woks'),
    path('api/live-posts/', views.live_posts_api, name='live_posts_api'),
    path('chat-ai/', views.chat_ai, name='chat_ai'),
    path('health/', views.health_check, name='health_check'),
]