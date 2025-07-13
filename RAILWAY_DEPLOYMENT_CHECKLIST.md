# Railway Deployment Checklist

## Pre-Deployment Checklist

### 1. Environment Variables
Ensure these are set in Railway Variables tab:

- [ ] `DEBUG=False`
- [ ] `EMAIL_HOST=smtp.gmail.com`
- [ ] `EMAIL_PORT=587`
- [ ] `EMAIL_USE_TLS=True`
- [ ] `EMAIL_HOST_USER=sabermrddzdot@gmail.com`
- [ ] `EMAIL_HOST_PASSWORD=foqv ltro aosq btbm`
- [ ] `DJANGO_SECRET_KEY=your_actual_secret_key`

### 2. Gmail Configuration
- [ ] 2-Factor Authentication enabled
- [ ] App Password generated for "Mail"
- [ ] App Password copied to `EMAIL_HOST_PASSWORD`

### 3. Files Check
- [ ] `requirements.txt` includes all dependencies
- [ ] `Procfile` exists and is correct
- [ ] `runtime.txt` specifies Python version
- [ ] `.env` file is not in `.gitignore`

### 4. Django Settings
- [ ] `ALLOWED_HOSTS` includes Railway domain
- [ ] `STATICFILES_STORAGE` is set to whitenoise
- [ ] `DEBUG=False` for production

## Post-Deployment Testing

### 1. Health Check
Visit: `https://your-railway-app.railway.app/health/`

Expected response:
```json
{
  "status": "healthy",
  "email_configured": true,
  "debug_mode": false,
  "allowed_hosts": ["your-domain.railway.app"],
  "email_backend": "django.core.mail.backends.smtp.EmailBackend",
  "email_host": "smtp.gmail.com",
  "email_port": 587,
  "email_use_tls": true
}
```

### 2. Contact Form Test
1. Go to `/contact`
2. Fill out the form
3. Submit and check for:
   - Success message appears
   - Email received in inbox
   - No JavaScript errors in console

### 3. Railway Logs Check
1. Go to Railway dashboard
2. Check deployment logs for:
   - No error messages
   - Email sending logs
   - Successful form submissions

## Common Issues & Solutions

### Issue: "Email service is not configured"
**Solution:** Check Railway Variables tab for email credentials

### Issue: "Authentication failed"
**Solution:** Regenerate Gmail App Password

### Issue: Form not submitting
**Solution:** Check browser console for JavaScript errors

### Issue: Static files not loading
**Solution:** Ensure whitenoise is in requirements.txt

## Testing Commands

### Local Testing
```bash
# Test email configuration
python test_email_config.py

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic
```

### Railway Testing
1. Deploy to Railway
2. Visit health check endpoint
3. Test contact form
4. Check Railway logs

## Monitoring

### Railway Logs
- Monitor for email sending errors
- Check for form submission logs
- Look for authentication issues

### Email Monitoring
- Check spam folder for test emails
- Verify email format and content
- Monitor for bounce backs

## Support

If issues persist:
1. Check Railway logs
2. Test health endpoint
3. Verify environment variables
4. Test email configuration locally
5. Contact developer with error details 