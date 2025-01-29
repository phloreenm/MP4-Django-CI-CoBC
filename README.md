# MP4 Full Stack E-Shop

This is a Django-based full-stack e-commerce web application that allows users to browse, purchase, and manage digital products. The project integrates Stripe for secure payments and supports user authentication for a seamless shopping experience.

---

## **Table of Contents**
- [Project Overview](#project-overview)
- [UX & UI Design](#ux-ui-design)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
- [Database Schema](#database-schema)
- [Stripe Payments](#stripe-payments)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)
- [Future Enhancements](#future-enhacements)

---

## **Project Overview**
This project was built as part of the Full Stack Web Development curriculum. It implements a **Django full-stack e-commerce system**, allowing users to:
- Browse and purchase **digital products** (e.g., e-books in `.pdf` format).
- Store purchase history for authenticated users.
- Handle payments securely using **Stripe**.
- Send confirmation emails upon successful orders.
- Manage product stock and availability.

---

## **Features**
### **Users & Authentication**
- User registration, login, and profile management.
- Secure authentication with Django Allauth.
- User purchase history tracking.

### **E-Commerce Functionality**
- Add/remove/update items in a shopping cart.
- Secure checkout process with **Stripe Payments**.
- Custom order confirmation emails.

### **Admin & Backend**
- Manage products via Django Admin.
- Track and process orders.

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
```

#### **Windows:**
```bash
python3 -m venv venv
venv\Scripts\activate
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Apply Migrations**
```bash
python3 manage.py migrate
```

### **4. Run the Server**
```bash
python3 manage.py runserver 
```
The app will be available at `http://127.0.0.1:8000/`.

---

## **Database Schema**
The application uses a **relational database** (SQLite locally, PostgreSQL in production).

### **Models**
- `Product`: Stores product details (name, description, price, stock).
- `Order`: Stores order details (user, total cost, payment status).
- `OrderLineItem`: Links products to an order.
- `UserProfile`: Stores user purchase history.

### **Database Migrations**
Run the following to apply database changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## **Stripe Payments**
### **Testing Interactively**
When testing payments, use a **Stripe test card**:
- **Card Number:** `4242 4242 4242 4242`
- **Expiry Date:** Any future date (`12/34`)
- **CVC:** Any 3-digit number (`123`)

### **Test Stripe Webhooks Locally**
#### **Stripe CLI**
1. Install Stripe CLI:
   ```bash
   brew install stripe/stripe-cli  # Mac
   sudo apt install stripe  # Linux
   ```
2. Log in:
   ```bash
   stripe login
   ```
3. Forward webhooks:
   ```bash
   stripe listen --forward-to localhost:8000/checkout/webhook/
   ```
4. Trigger a test event:
   ```bash
   stripe trigger checkout.session.completed
   ```

#### **Fix Stripe Keys Issues**
If Stripe keys don’t work, check for **environment variables**:
```bash
env | grep STRIPE
```
To unset global variables:
```bash
unset STRIPE_PUBLIC_KEY
unset STRIPE_SECRET_KEY
```
Then restart Django:
```bash
python manage.py runserver
```

---

## **Testing**
The project includes both **manual and automated tests**.

### **Manual Testing**
- Tested across **multiple browsers** (Chrome, Firefox).
- Validated with **Chrome DevTools** for responsive design.
- Ensured that checkout and payments work correctly.

### **Unit & Integration Testing**
Run Django tests using:
```bash
python manage.py test
```

<!-- ### **Code Validation**
- **HTML Validation**: [W3C Validator](https://validator.w3.org/)
- **CSS Validation**: [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)
- **Python Code Linting**: `flake8` -->

---

## **Deployment**
<!-- This project is deployed on **Heroku**. -->

### **Steps to Deploy**
1. Create a **Heroku App**:
   ```bash
   heroku create your-app-name
   ```
2. Add the **Heroku Postgres Add-on**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```
3. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY='your-secret-key'
   heroku config:set STRIPE_PUBLIC_KEY='your-public-key'
   heroku config:set STRIPE_SECRET_KEY='your-secret-key'
   ```
4. Push the project to Heroku:
   ```bash
   git push heroku main
   ```
5. Run database migrations:
   ```bash
   heroku run python manage.py migrate
   ```
6. Open the deployed app:
   ```bash
   heroku open
   ```

---

## **Credits**
### **Code Snippets & Libraries**
- **Bootstrap 5.3** (for responsive UI)
- **Stripe API** (for payments)
- **python-decouple** (for environment variables)
- **django-countries** (for shipping addresses)
- **django-crispy-forms & crispy-bootstrap5** (for form styling)

---

## **License**
This project is licensed under the MIT License.
```

