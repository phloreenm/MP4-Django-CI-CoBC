# checkout/tests.py

from django.test import TestCase
import smtplib
import ssl
import os

class SMTPConnectionTest(TestCase):
    def test_smtp_connection(self):
        # Create an SSL context using the default CA certificates
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls(context=context)
                # Replace these with your actual email credentials
                server.login(os.environ.get("EMAIL_HOST_USER"), os.environ.get("EMAIL_HOST_PASSWORD"))
                # If we reach here, the connection is successful.
                print("Connected and logged in successfully!")
        except Exception as e:
            self.fail(f"SMTP connection failed: {e}")