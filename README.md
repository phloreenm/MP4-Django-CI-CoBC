Below is the complete content for your new README-data-si-ora-actualizarii.md file. You can copy and paste this as one complete markdown document. (Be sure to update the “Last Updated” date/time as needed.)

# MP4 Full Stack E-Shop  
*Last Updated: February 04, 2025, 14:00*

This is a Django-based full-stack e-commerce web application that allows users to browse, purchase, and manage digital products. The project integrates Stripe for secure payments and supports user authentication for a seamless shopping experience. The application is designed in a modular fashion—with separate apps for Checkout, Orders, Profiles, and (if needed) a Dashboard.

---

## **Table of Contents**
- [MP4 Full Stack E-Shop](#mp4-full-stack-e-shop)
  - [**Table of Contents**](#table-of-contents)
  - [**Project Overview**](#project-overview)
  - [**UX \& UI Design**](#ux--ui-design)
  - [**Features**](#features)
    - [**Users \& Authentication**](#users--authentication)
    - [**E-Commerce Functionality**](#e-commerce-functionality)
    - [**Orders Module**](#orders-module)
    - [**Admin \& Backend**](#admin--backend)
    - [**Security \& Performance**](#security--performance)
  - [**Technologies Used**](#technologies-used)
  - [**Installation \& Setup**](#installation--setup)
    - [**1. Create a Virtual Environment**](#1-create-a-virtual-environment)
      - [**Linux/macOS:**](#linuxmacos)

---

## **Project Overview**
This project was built as part of the Full Stack Web Development curriculum. It implements a **Django full-stack e-commerce system**, allowing users to:
- Browse and purchase **digital products** (e.g., e-books in `.pdf` format).
- Place orders through a secure checkout process with **Stripe Payments**.
- Receive confirmation emails upon successful orders.
- Manage purchase history via a dedicated Orders module.
- Support both authenticated and unauthenticated users during checkout:
  - Registered users have their orders linked to their account.
  - Unregistered users can look up orders using an order number and email address.

---

## **UX & UI Design**
- **Responsive Design:**  
  The frontend uses Bootstrap 5.3 for responsiveness across devices.
- **Navigation:**  
  The navigation bar adapts based on the user’s role:
  - **Admins/Sellers:** See an “Orders Summary” page with full CRUD controls.
  - **Regular Clients:** See their own orders ("My Orders") with options to cancel or request alteration if the order is pending.
  - **Unauthenticated Users:** Are directed to an Order Lookup page to find their order using order number and email.

---

## **Features**
### **Users & Authentication**
- User registration, login, and profile management using Django Allauth.
- Option for unregistered users to place orders and later look them up via order number and email.

### **E-Commerce Functionality**
- Shopping cart functionality (add, remove, update items).
- Secure checkout process integrated with Stripe for payments.
- Custom order confirmation emails.

### **Orders Module**
- **Order Creation:**  
  Orders are created during checkout and stored in a dedicated Orders app.
- **Role-Based Order Viewing:**  
  - **Admins:** See all orders with full CRUD (Create, Read, Update, Delete) controls.
  - **Sellers:** See all orders (or a filtered subset) sorted chronologically, with administrative controls.
  - **Regular Users:** See only their own orders (My Orders) and can view details or request cancellation/alteration if the order is pending.
- **Order Lookup for Unauthenticated Users:**  
  Unregistered users can look up their order by providing the order number and the email used at checkout.

### **Admin & Backend**
- Manage products via Django Admin.
- Orders are managed via the dedicated Orders app.
- Custom order confirmation emails and notifications.

### **Security & Performance**
- Secure environment variables with **python-decouple**.
- Uses **django-countries** for shipping addresses.
- Responsive design with **Bootstrap 5.3**.

---

## **Technologies Used**
- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5.3
- **Database:** PostgreSQL / SQLite (for local development)
- **Payments:** Stripe API
- **Form Handling:** Django Crispy Forms + crispy-bootstrap5
- **Security:** Django Allauth, Python-Decouple
- **Version Control:** Git & GitHub

---

## **Installation & Setup**

### **1. Create a Virtual Environment**
#### **Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate

Windows:

python3 -m venv venv
venv\Scripts\activate

2. Install Dependencies

pip install -r requirements.txt

3. Apply Migrations

python3 manage.py makemigrations
python3 manage.py migrate

4. Run the Server

python3 manage.py runserver

The app will be available at http://127.0.0.1:8000/.

Database Schema

The application uses a relational database (SQLite locally, PostgreSQL in production).

Models
	•	Product:
Stores product details (name, description, price, stock).
	•	Order:
Stores order details such as order number, shipping information, total cost, payment status, and order status. For authenticated users, orders are linked to their account.
	•	OrderLineItem:
A one-to-many relationship linking products to an order.
	•	UserProfile:
(Implemented in the Profiles app) Stores additional user information and purchase history.

Database Migrations

Run the following to apply database changes:

python3 manage.py makemigrations
python3 manage.py migrate

Stripe Payments

Testing Interactively

When testing payments, use a Stripe test card:
	•	Card Number: 4242 4242 4242 4242
	•	Expiry Date: Any future date (e.g., 12/34)
	•	CVC: Any 3-digit number (e.g., 123)

Test Stripe Webhooks Locally

Stripe CLI
	1.	Install Stripe CLI:

brew install stripe/stripe-cli  # Mac
sudo apt install stripe  # Linux


	2.	Log in:

stripe login


	3.	Forward webhooks:

stripe listen --forward-to localhost:8000/checkout/webhook/


	4.	Trigger a test event:

stripe trigger checkout.session.completed



Fix Stripe Keys Issues

Check for environment variables:

env | grep STRIPE

Unset global variables if necessary:

unset STRIPE_PUBLIC_KEY
unset STRIPE_SECRET_KEY

Then restart Django:

python manage.py runserver

Orders Module

Orders Summary & Lookup
	•	Orders Summary (Admins & Sellers):
Administrators and sellers can view all orders with full CRUD controls (Edit, Delete, etc.).
URL: /orders/summary/
	•	My Orders (Clients):
Regular users see only their own orders.
URL: /orders/my-orders/
	•	Order Lookup (Unauthenticated Users):
Unregistered users can find their order by entering the order number and the email provided at checkout.
URL: /orders/lookup/

The Orders module is implemented in a dedicated app using proper relational links (one-to-many from Order to OrderLineItem) and role-based views.

Navbar Customization

The navigation bar dynamically directs users to the appropriate Orders page based on their role. For example, the Orders link in the navbar:
	•	Admins/Sellers: Link to the Orders Summary page.
	•	Regular Users: Link to the My Orders page.
	•	Unauthenticated Users: Link to the Order Lookup page.

A custom template filter (e.g., in_group) is used to check group membership, and the slice filter is used to conditionally assign CSS classes.

Testing

The project includes both manual and automated tests.

Manual Testing
	•	Tested on multiple browsers (Chrome, Firefox).
	•	Verified with Chrome DevTools for responsiveness.
	•	Confirmed that checkout, payments, and order management (including lookup for unauthenticated users) work correctly.

Unit & Integration Testing

Run Django tests using:

python manage.py test

Deployment

Steps to Deploy
	1.	Create a Heroku App:

heroku create your-app-name


	2.	Add the Heroku Postgres Add-on:

heroku addons:create heroku-postgresql:hobby-dev


	3.	Set environment variables:

heroku config:set SECRET_KEY='your-secret-key'
heroku config:set STRIPE_PUBLIC_KEY='your-public-key'
heroku config:set STRIPE_SECRET_KEY='your-secret-key'


	4.	Push the project to Heroku:

git push heroku main


	5.	Run database migrations:

heroku run python manage.py migrate


	6.	Open the deployed app:

heroku open

Credits

Code Snippets & Libraries
	•	Bootstrap 5.3 for responsive UI.
	•	Stripe API for payments.
	•	python-decouple for environment variable management.
	•	django-countries for shipping addresses.
	•	django-crispy-forms & crispy-bootstrap5 for form styling.
	•	Django Allauth for authentication.

Future Enhancements
	•	Enhanced Order Workflow:
Introduce additional order statuses (e.g., processing, shipped, delivered, refunded) with validation for state transitions.
	•	Email Notifications:
Automatically send confirmation emails and status updates via Django signals.
	•	Digital Products Integration:
Implement a “My Products” view for clients to download purchased PDFs.
	•	Detailed Dashboard:
Create comprehensive dashboards for admins and sellers with filtering, sorting, and export functionality.
	•	Advanced Order Lookup:
Enhance security for the order lookup process by including verification tokens.
	•	Profiles & User Management:
Expand the Profiles app for more detailed user settings and purchase history.

This document summarizes the current implementation and structure of the MP4 Full Stack E-Shop, including the modular Orders app with role-based views and order lookup functionality.

---

You can save this content in a file named `README-data-si-ora-actualizarii.md`. Let me know if you need further adjustments or additional sections!