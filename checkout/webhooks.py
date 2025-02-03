from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def webhook(request):
    """Listen for Stripe webhooks."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
        )
    except ValueError as e:
        # Invalid payload
        logger.error("Invalid payload", exc_info=True)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error("Signature verification failed", exc_info=True)
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        logger.info("Payment Succeeded: %s", payment_intent.get('id'))
        # + logic to let the user know that the payment succeeded
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        logger.warning("Payment failed: %s", payment_intent.get('id'))
        # + logic to let the user know that the payment failed
    else:
        # Log any unhandled event types for debugging
        logger.info("Unhandled event type: %s", event['type'])

    return HttpResponse(status=200)