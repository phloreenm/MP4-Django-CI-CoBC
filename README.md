# MP4 Full Stack E-Shop  
*Last Updated: February 04, 2025, 18:00*

This is a Django-based full-stack e-commerce web application that allows users to browse, purchase, and manage digital products. The project integrates Stripe for secure payments and supports user authentication for a seamless shopping experience. The application is designed in a modular fashion—with separate apps for Checkout, Orders, Profiles (User Account Management), and (if needed) a Dashboard.

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
		- [**Profiles Module**](#profiles-module)
		- [**Admin \& Backend**](#admin--backend)
		- [**Security \& Performance**](#security--performance)
	- [**Technologies Used**](#technologies-used)
	- [**Installation \& Setup**](#installation--setup)
		- [**1. Create a Virtual Environment**](#1-create-a-virtual-environment)
			- [**Linux/macOS:**](#linuxmacos)

---

## **Project Overview**
This project was built as part of the Full Stack Web Development curriculum. It implements a **Django full-stack e-commerce system**, allowing users to:
- Browse and purchase **digital products** (for example, e-books in `.pdf` format).
- Place orders through a secure checkout process integrated with **Stripe Payments**.
- Receive confirmation emails upon successful orders.
- Manage purchase history and access digital downloads via the dedicated Orders module.
- Manage their account via a Profiles module that extends the built‑in User model.
- Support both authenticated and unauthenticated users during checkout:
  - Registered users have their orders linked to their account.
  - Unregistered users can look up orders using an order number and email address.

---

## **UX & UI Design**
- **Responsive Design:**  
  The frontend uses Bootstrap 5.3 to ensure responsiveness across devices.
- **Navigation:**  
  The navigation bar adapts based on the user’s role:
  - **Admins/Sellers:** See an “Orders Summary” page with full CRUD controls.
  - **Regular Users:** See their own orders ("My Orders") with options (e.g., cancel or request alterations if pending).
  - **Unauthenticated Users:** Are directed to an Order Lookup page to retrieve order details.
- **Profiles Section:**  
  Registered users can access their "My Profile" section to view and edit personal details as well as see their purchase history and download digital products.

---

## **Features**
### **Users & Authentication**
- User registration, login, and profile management using Django Allauth.
- For unregistered users, an order lookup functionality is provided so they can later retrieve order details using an order number and email.

### **E-Commerce Functionality**
- Shopping cart functionality: add, remove, and update items.
- Secure checkout process with Stripe for payments.
- Custom order confirmation emails with download instructions for digital products.

### **Orders Module**
- **Order Creation:**  
  Orders are created during checkout and stored in a dedicated Orders app.
- **Role-Based Order Viewing:**  
  - **Admins:** Can view all orders with full CRUD (Create, Read, Update, Delete) operations.
  - **Sellers:** Can view all orders (or a filtered subset) with administrative controls.
  - **Regular Users:** Can view only their own orders ("My Orders") and, if pending, request cancellation or alteration.
- **Order Lookup for Unauthenticated Users:**  
  Unregistered users can find their orders by entering the order number and the email used during checkout.
- **Digital Downloads:**  
  Once an order is approved/delivered, customers can download their digital product (e.g., PDF) via dynamically generated links.

### **Profiles Module**
- **Profile Model:**  
  A Profile model is implemented to extend the built-in User model. It includes additional fields such as phone number, street address, city, postcode, county, country, bio, profile picture, and date of birth.
- **Automatic Profile Creation:**  
  A signal (and optionally middleware) automatically creates a Profile for every new user. For existing users without a profile, a management command or middleware ensures consistency.
- **Profile Management:**  
  Users can view their profile in "My Profile" and update their information via an "Edit Profile" page.

### **Admin & Backend**
- Products are managed through Django Admin.
- Orders are managed through a dedicated Orders app with role-based access.
- Profiles can be managed via a custom Profiles admin interface.
- Custom email notifications (to be implemented) inform users when orders are confirmed and digital downloads become available.

### **Security & Performance**
- Secure management of environment variables with **python-decouple**.
- Use of **django-countries** for shipping addresses.
- Responsive design with **Bootstrap 5.3**.
- Role-based access to both orders and profiles to ensure data integrity.

---

## **Technologies Used**
- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5.3
- **Database:** PostgreSQL (production) or SQLite (for local development)
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
```

Windows:
```
python3 -m venv venv
venv\Scripts\activate
```

2. Install Dependencies
```
pip install -r requirements.txt
```

3. Apply Migrations
```
python3 manage.py makemigrations
python3 manage.py migrate
```

4. Run the Server
```
python3 manage.py runserver
```
The app will be available at http://127.0.0.1:8000/.

Database Schema

The application uses a relational database (SQLite locally, PostgreSQL in production).

Models
	•	Product:
Stores product details (name, description, price, stock).
	•	Order:
Stores order details such as order number, user (if authenticated), shipping information, total cost, payment status, order status (e.g., pending, approved, delivered, canceled), and comments.
	•	OrderLineItem:
Represents a one-to-many relationship linking products to an order.
	•	Profile:
Extends the built-in User model with additional fields: phone number, street address, city, postcode, county, country, bio, profile picture, and date of birth.

Database Migrations

Apply the changes with:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Stripe Payments

Testing Interactively

When testing payments, use a Stripe test card:
	•	Card Number: 4242 4242 4242 4242
	•	Expiry Date: Any future date (e.g., 12/34)
	•	CVC: Any 3-digit number (e.g., 123)

Test Stripe Webhooks Locally

Stripe CLI
	1.	Install Stripe CLI:
```
brew install stripe/stripe-cli  # Mac
sudo apt install stripe  # Linux
```

	2.	Log in:
```
stripe login
```

	3.	Forward webhooks:
```
stripe listen --forward-to localhost:8000/checkout/webhook/
```

	4.	Trigger a test event:
```
stripe trigger checkout.session.completed
```


Fix Stripe Keys Issues

Check environment variables:
```
env | grep STRIPE
```
Unset global variables if necessary:
```
unset STRIPE_PUBLIC_KEY
unset STRIPE_SECRET_KEY
```
Then restart Django:
```
python3 manage.py runserver
```


Orders Module

Orders Summary & Lookup
	•	Orders Summary (Admins & Sellers):
Administrators and sellers can view all orders with full CRUD controls.
URL: /orders/summary/
	•	My Orders (Clients):
Regular users see only their own orders.
URL: /orders/my-orders/
	•	Order Lookup (Unauthenticated Users):
Unregistered users can look up their orders by providing the order number and email.
URL: /orders/lookup/
	•	Digital Downloads:
Once an order is approved/delivered, customers can download their digital product via dynamically generated links.
Example Download URL: /orders/download/<order_number>/

Key Views:
	•	my_orders: Displays the logged-in user’s orders.
	•	order_detail: Shows details for a specific order.
	•	cancel_order: Allows users to cancel a pending order.
	•	orders_summary: For admins/sellers to view all orders.
	•	order_lookup: Lets unauthenticated users find their order.
	•	download_product: Serves the digital file for approved orders.
	•	Additional views for editing, deleting, or altering orders (subject to role-based permissions).

Known Bug: Order Total Display
	•	Issue:
In the Orders module (both in the admin panel and on the order detail page), the total sum of the order sometimes appears as 0 regardless of the actual items.
	•	Status:
This is a known issue that will be addressed in a future update by ensuring the order totals are calculated and saved correctly when line items are added.

	•	Issue:
After a succesfull/failed order, there is a script to send a confirmation email. 
	•	Status:
I eventually sorted it with a solution I found here: https://stackoverflow.com/questions/75269008/getting-ssl-error-when-sending-email-via-django

Profiles Module

Profile Model
	•	Relationship:
A one-to-one relationship with the Django User model.
	•	Additional Fields:
	•	phone_number
	•	street_address
	•	city
	•	postcode
	•	county
	•	country
	•	bio
	•	profile_picture
	•	date_of_birth

Key Views:
	•	my_profile: Displays the logged-in user’s profile and account details.
	•	edit_profile: Allows users to update their profile information.

URL Patterns:
	•	My Profile: /profiles/my-profile/
	•	Edit Profile: /profiles/edit-profile/

Automatic Profile Creation
	•	Signals:
A signal in profiles/signals.py automatically creates a Profile when a new user is registered.
	•	Middleware (Optional):
A middleware (in profiles/middleware.py) ensures that every authenticated user has a Profile on each request.
	•	Management Command (Optional):
A one-time command can be used to create missing profiles for existing users.

Navbar Customization

The navigation bar dynamically directs users to the appropriate Orders and Profiles pages based on their authentication status:
	•	Admins/Sellers:
See the Orders Summary.
	•	Regular Users:
See My Orders.
	•	Unauthenticated Users:
See the Order Lookup page.
	•	My Account:
The “My Account” link (for profiles) appears only if the user is logged in.
Example snippet from the navbar:
```
{% if user.is_authenticated %}
  <li class="nav-item">
    <a href="{% url 'profiles:my_profile' %}" class="nav-link {% if request.path|slice:"0:13" == '/profiles/my' %}text-secondary{% else %}text-white{% endif %}">
      <i class="bi bi-person-circle d-block mx-auto mb-1"></i>
      My Account
    </a>
  </li>
{% endif %}
```

Testing

The project includes both manual and automated tests.

Manual Testing
	•	Tested on multiple browsers (Chrome, Firefox).
	•	Verified responsiveness using Chrome DevTools.
	•	Confirmed that checkout, payments, order management (including lookup for unauthenticated users), and profile management work correctly.

Unit & Integration Testing

Run Django tests using:
```
python3 manage.py test
```

Deployment

Steps to Deploy
	1.	Create a Heroku App:
```
heroku create your-app-name
```

	2.	Add the Heroku Postgres Add-on:
```
heroku addons:create heroku-postgresql:hobby-dev
```

	3.	Set Environment Variables:
```
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set STRIPE_PUBLIC_KEY='your-public-key'
heroku config:set STRIPE_SECRET_KEY='your-secret-key'
```

	4.	Push the Project to Heroku:
```
git push heroku main
```

	5.	Run Database Migrations:
```
heroku run python manage.py migrate
```

	6.	Open the Deployed App:
```
heroku open
```


Known Issues & Bug Fixes
	•	Missing Profiles on Login:
Some users created before the Profiles app was set up do not have an associated Profile, causing a RelatedObjectDoesNotExist: User has no profile error.
Solution:
	•	A signal in profiles/signals.py automatically creates a Profile when a new user is registered.
	•	Additionally, a middleware (profiles/middleware.py) can be added to ensure every authenticated user has a Profile on each request.
	•	For existing users, a management command can be used to create missing profiles.
	•	CSRF Token Errors:
Ensured that all POST forms include {% csrf_token %} and that CSRF middleware is enabled.
	•	Dynamic Download Links:
Digital product downloads are served via a dedicated view that checks the order status, ensuring that only approved orders allow downloads.
	•	Order Total Display Bug:
In the Orders module, the total sum for an order sometimes appears as 0 (in both the admin panel and on the order detail page) regardless of the actual items. This is a known issue that will be addressed in future updates by recalculating and saving order totals correctly when OrderLineItems are created.

Credits

Code Snippets & Libraries
	•	Bootstrap 5.3: For responsive UI.
	• 	[Nav Bar Bootsrap 5](https://getbootstrap.com/docs/5.0/components/navbar/)
	•	Stripe API: For secure payment processing.
	•	python-decouple: For managing environment variables.
	•	django-countries: For handling country fields.
	•	django-crispy-forms & crispy-bootstrap5: For form styling.
	•	Django Allauth: For authentication.
	•	Custom Middleware & Signals: For ensuring every user has an associated Profile.

Future Enhancements
	•	Enhanced Order Workflow:
Introduce additional order statuses (e.g., processing, shipped, delivered, refunded) with state transition validation.
	•	Email Notifications:
Automatically send confirmation emails and status updates via Django signals.
	•	Digital Products Integration:
Expand the “My Products” functionality—potentially integrate it within the Profiles module for a unified “My Account” experience.
	•	Detailed Dashboard:
Develop comprehensive dashboards for admins and sellers with filtering, sorting, and export capabilities.
	•	Advanced Order Lookup:
Enhance security for order lookup by including verification tokens.
	•	Extended Profiles:
Further extend the Profiles module with additional user settings, purchase history, and personalized recommendations.
