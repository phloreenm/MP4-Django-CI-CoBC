from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_confirmation_email(order):
    """
    Sends an email confirming that the order was received.
    """
    subject = render_to_string("orders/emails/order_confirmation_subject.txt", {"order": order}).strip()
    message = render_to_string("orders/emails/order_confirmation_body.txt", {"order": order})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.email])

def send_order_approval_email(order):
    """
    Sends an email to the customer when an order is approved (confirmed by the seller).
    This email can include download links for digital products.
    """
    subject = render_to_string("orders/emails/order_approval_subject.txt", {"order": order}).strip()
    message = render_to_string("orders/emails/order_approval_body.txt", {"order": order})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.email])

def send_order_cancellation_email(order):
    """
    Sends an email to the customer when an order is canceled.
    """
    subject = render_to_string("orders/emails/order_cancellation_subject.txt", {"order": order}).strip()
    message = render_to_string("orders/emails/order_cancellation_body.txt", {"order": order})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.email])