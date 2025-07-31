# Heroku Deployment Guide

This guide will help you deploy your Django e-commerce application to Heroku.

## Prerequisites

1. **Heroku Account**: Create account at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure your code is committed to git

## Step 1: Install Heroku Dependencies

```bash
pip3 install dj-database-url gunicorn psycopg2-binary whitenoise
```

## Step 2: Create Heroku App

```bash
# Login to Heroku
heroku login

# Create new app (replace 'your-app-name' with your desired name)
heroku create your-app-name

# Add PostgreSQL database
heroku addons:create heroku-postgresql:hobby-dev
```

## Step 3: Set Environment Variables on Heroku

```bash
# Required variables
heroku config:set ENVIRONMENT=production
heroku config:set SECRET_KEY='your-very-long-secret-key-here'
heroku config:set DEBUG=False

# Stripe configuration
heroku config:set STRIPE_PUBLIC_KEY='pk_live_your_public_key'
heroku config:set STRIPE_SECRET_KEY='sk_live_your_secret_key'
heroku config:set STRIPE_WH_SECRET='whsec_your_webhook_secret'

# Set allowed hosts (replace with your app name)
heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'

# Optional: Gmail configuration (if you want emails in production)
heroku config:set EMAIL_HOST_USER='your-email@gmail.com'
heroku config:set EMAIL_HOST_PASSWORD='your-16-char-app-password'
```

## Step 4: Deploy to Heroku

```bash
# Add Heroku remote (if not already added)
heroku git:remote -a your-app-name

# Push code to Heroku
git push heroku main
```

## Step 5: Run Database Migrations

```bash
# Run migrations on Heroku
heroku run python manage.py migrate

# Create superuser account
heroku run python manage.py createsuperuser
```

## Step 6: Collect Static Files

```bash
# Collect static files
heroku run python manage.py collectstatic --noinput
```

## Step 7: Open Your App

```bash
heroku open
```

## Important Notes

### Database Content
- **Fresh start**: Heroku will have an empty PostgreSQL database
- **No automatic data transfer**: Your local SQLite data won't be copied
- **You'll need to**:
  - Create a new superuser account
  - Re-add products through the admin panel
  - Set up any initial data

### Environment Differences
- **Local**: Uses SQLite + Console email backend
- **Heroku**: Uses PostgreSQL + Gmail SMTP (if configured)

### Troubleshooting

#### Check Heroku Logs
```bash
heroku logs --tail
```

#### Common Issues
1. **Missing environment variables**: Set all required config vars
2. **Static files not loading**: Run `collectstatic` command
3. **Database errors**: Run migrations with `heroku run python manage.py migrate`
4. **Import errors**: Ensure all dependencies are in `requirements.txt`

#### Verify Configuration
```bash
# Check environment variables
heroku config

# Check app status
heroku ps

# Access Django shell on Heroku
heroku run python manage.py shell
```

### Files Created for Heroku
- `Procfile`: Tells Heroku how to run your app
- `runtime.txt`: Specifies Python version
- `requirements.txt`: Updated with Heroku dependencies

### Security Notes
- Never commit secret keys to git
- Use environment variables for all sensitive data
- Ensure DEBUG=False in production
- Use HTTPS URLs for webhooks in production
