# Contact Form Troubleshooting Guide

## Common Issues and Solutions

### 1. Email Configuration Issues

#### Problem: "Email service is not configured"
**Solution:**
- Ensure `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are set in Railway environment variables
- Go to Railway dashboard → Your project → Variables tab
- Add these variables:
  ```
  EMAIL_HOST_USER=sabermrddzdot@gmail.com
  EMAIL_HOST_PASSWORD=foqv ltro aosq btbm
  ```

#### Problem: "Email authentication failed"
**Solution:**
- Verify Gmail App Password is correct
- Enable 2-Factor Authentication on your Gmail account
- Generate a new App Password:
  1. Go to Google Account settings
  2. Security → 2-Step Verification → App passwords
  3. Generate new password for "Mail"
  4. Update `EMAIL_HOST_PASSWORD` in Railway

### 2. JavaScript Errors

#### Problem: Form not submitting
**Check:**
- Open browser developer tools (F12)
- Look for JavaScript errors in Console tab
- Ensure all required fields are filled

#### Problem: Mobile menu not working
**Solution:**
- Fixed in the latest update
- Check if `mobile-menu-btn` and `menu-icon` IDs exist

### 3. CSRF Token Issues

#### Problem: "CSRF verification failed"
**Solution:**
- Ensure `{% csrf_token %}` is present in the form
- Check if `X-CSRFToken` header is being sent
- Verify Django middleware includes `CsrfViewMiddleware`

### 4. Railway Deployment Issues

#### Problem: Static files not loading
**Solution:**
- Run `python manage.py collectstatic` locally
- Ensure `whitenoise` is in requirements.txt
- Check `STATICFILES_STORAGE` setting

#### Problem: Environment variables not loading
**Solution:**
- Verify `.env` file is not in `.gitignore`
- Check Railway Variables tab
- Ensure `python-dotenv` is in requirements.txt

## Testing Steps

### 1. Test Email Configuration
```bash
python test_email_config.py
```

### 2. Test Form Locally
1. Run `python manage.py runserver`
2. Go to `/contact`
3. Fill out form and submit
4. Check console for errors

### 3. Test on Railway
1. Deploy to Railway
2. Go to your Railway URL + `/contact`
3. Test form submission
4. Check Railway logs for errors

## Debug Information

### Check Railway Logs
1. Go to Railway dashboard
2. Click on your deployment
3. Go to "Logs" tab
4. Look for error messages

### Common Error Messages

1. **"Email credentials not configured"**
   - Environment variables missing

2. **"Authentication failed"**
   - Gmail App Password incorrect

3. **"Connection error"**
   - Network/firewall issues
   - SMTP port blocked

4. **"Invalid header"**
   - Special characters in form fields
   - Malformed email address

## Environment Variables Checklist

Ensure these are set in Railway:

```
DEBUG=False
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=sabermrddzdot@gmail.com
EMAIL_HOST_PASSWORD=foqv ltro aosq btbm
DJANGO_SECRET_KEY=your_actual_secret_key
```

## Gmail Setup Requirements

1. **2-Factor Authentication**: Must be enabled
2. **App Password**: Generate specific password for this app
3. **Less Secure Apps**: Not needed with App Password
4. **SMTP Settings**: Use port 587 with TLS

## Contact Form Features

- ✅ AJAX submission (no page reload)
- ✅ Real-time validation
- ✅ Success/error messages
- ✅ Loading states
- ✅ CSRF protection
- ✅ Email notifications
- ✅ Mobile responsive

## Support

If issues persist:
1. Check Railway logs
2. Test email configuration
3. Verify environment variables
4. Contact developer with error details 