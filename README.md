# Inspair.Health - Medical Web Application

A Django-based medical/health web application with AI chat assistant and daily health posts.

## Features

- **Home Page**: Modern landing page with animated background effects
- **AI Chat**: Medical AI assistant with conversation memory and language detection
- **Daily Posts**: Health news and articles with live API integration
- **About & Contact**: Information pages
- **Responsive Design**: Works on desktop and mobile devices

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# For live health news (optional)
NEWSAPI_KEY=your_newsapi_key_here

# For AI chat functionality (optional)
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

#### Getting API Keys:

**NewsAPI Key:**
1. Go to [NewsAPI.org](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key from the dashboard

**OpenRouter API Key:**
1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for an account
3. Get your API key from the dashboard

### 3. Run the Application

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the application.

## API Integration

### Daily Posts API
- **Endpoint**: `/api/live-posts/`
- **Method**: POST
- **Purpose**: Fetches live health news from NewsAPI
- **Fallback**: Returns sample articles if API key is not configured

### Chat AI API
- **Endpoint**: `/chat-ai/`
- **Method**: POST
- **Purpose**: Provides AI medical assistance
- **Fallback**: Returns predefined responses if API key is not configured

## Features Without API Keys

The application will work without API keys:
- **Daily Posts**: Shows sample health articles
- **AI Chat**: Provides fallback medical responses
- All other features work normally

## File Structure

```
clinic/
├── templates/clinic/
│   ├── home.html          # Landing page
│   ├── chat_box.html      # AI chat interface
│   ├── daily_posts.html   # Health news page
│   ├── about.html         # About page
│   └── contact.html       # Contact page
├── views.py               # Backend views and API endpoints
├── urls.py                # URL routing
└── models.py              # Database models

mysite/
├── settings.py            # Django settings
└── urls.py                # Main URL configuration
```

## Technologies Used

- **Backend**: Django 4.x
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Tailwind CSS
- **Icons**: Font Awesome
- **APIs**: NewsAPI, OpenRouter AI

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## License

This project is for educational purposes. 