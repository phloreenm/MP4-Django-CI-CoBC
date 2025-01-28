

Create virtual enviroment in bash: python3 -m venv venv
Linux: source venv/bin/activate
Windows: venv\Scripts\activate

pip freeze > requirements.txt
pip install -r requirements.txt


## Stripe payments test:
### Testing interactively
When testing interactively, use a card number, such as 4242 4242 4242 4242. Enter the card number in the Dashboard or in any payment form.
    Use a valid future date, such as 12/34.
    Use any three-digit CVC (four digits for American Express cards).
    Use any value you like for other form fields.

### Test Stripe Webhooks Locally
#### Stripe CLI
- Install locally: brew install stripe/stripe-cli/stripe
- Login locally: "stripe login" and follow steps to confirm your login pairing
- Forward webhooks to local server: stripe listen --forward-to localhost:8000/checkout/webhook/
#### Test webhooks:
- Test sending an event: stripe trigger checkout.session.completed
- Check Django console 

#### If Stripe Keys don't work
Check for Globally Set Environment Variables
- Run the following command to list all environment variables in your shell: ''env | grep STRIPE''
- Unset them using: ''unset STRIPE_PUBLIC_KEY
unset STRIPE_SECRET_KEY''
Restart Django and Your Shell

# Credits
## Code Snippets
 - Boostrap 5.3 
 - Stripe
 - python-decouple