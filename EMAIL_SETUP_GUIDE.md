# Email Configuration Guide

## Current Setup
Currently, the project uses **console email backend** for development. Emails are displayed in the terminal instead of being sent.

## Gmail Configuration for Production

### Step 1: Enable 2-Step Verification
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Turn on **2-Step Verification**
3. Verify your phone number

### Step 2: Create App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select **Mail** and your device
3. Copy the **16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 3: Environment Variables
Create a `.env` file or set these variables:

```bash
# Gmail Configuration
EMAIL_HOST_USER=yourname@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop  # Your app password
ENVIRONMENT=production  # Switches from console to SMTP
```

### Step 4: Test Email Setup
```python
# In Django shell (python manage.py shell)
from django.core.mail import send_mail

send_mail(
    'Test Subject',
    'Test message.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

## Alternative Email Services (Recommended for Production)

### SendGrid
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

### Mailgun
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-mailgun-username'
EMAIL_HOST_PASSWORD = 'your-mailgun-password'
```

### Amazon SES
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-ses-access-key'
EMAIL_HOST_PASSWORD = 'your-ses-secret-key'
```

## Current Email Functions

### Order Confirmation Email
- **File**: `orders/emails.py`
- **Function**: `send_order_confirmation_email(order)`
- **Template**: `orders/emails/order_confirmation_subject.txt`
- **Template**: `orders/emails/order_confirmation_body.txt`

### Order Approval Email
- **Function**: `send_order_approval_email(order)`
- **Used**: When admin approves an order

### Order Cancellation Email
- **Function**: `send_order_cancellation_email(order)`
- **Used**: When order is cancelled

## Troubleshooting

### Common Gmail Issues
1. **"Authentication Required"** → Check app password
2. **"Less secure app access"** → Use app passwords instead
3. **"Suspicious activity"** → Verify from Gmail security tab

### Testing in Development
1. Check terminal output for console emails
2. Look for email content in Django logs
3. Use `python manage.py shell` for manual testing

## Security Notes
- Never commit real email credentials to Git
- Use environment variables for sensitive data
- Consider using dedicated email services for production
- Monitor email sending limits and costs
