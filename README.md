# MP4 Full Stack E-Shop

This is a Django-based full-stack e-commerce web application that allows users to browse, purchase, and manage digital products. The project integrates Stripe for secure payments and supports user authentication for a seamless shopping experience.

---

## **Table of Contents**
- [MP4 Full Stack E-Shop](#mp4-full-stack-e-shop)
  - [**Table of Contents**](#table-of-contents)
  - [**Project Overview**](#project-overview)
  - [**Features**](#features)
    - [**Users \& Authentication**](#users--authentication)
    - [**E-Commerce Functionality**](#e-commerce-functionality)
    - [**Admin \& Backend**](#admin--backend)
    - [**Security \& Performance**](#security--performance)
  - [**Technologies Used**](#technologies-used)
  - [**Installation \& Setup**](#installation--setup)
    - [**1. Create a Virtual Environment**](#1-create-a-virtual-environment)
      - [**Linux/macOS:**](#linuxmacos)
      - [**Windows:**](#windows)
    - [**2. Install Dependencies**](#2-install-dependencies)
    - [**3. Apply Migrations**](#3-apply-migrations)
    - [**4. Run the Server**](#4-run-the-server)
  - [**Database Schema**](#database-schema)
  - [**Stripe Payments**](#stripe-payments)
  - [**Testing**](#testing)
  - [**Deployment**](#deployment)
  - [**UX \& UI Design**](#ux--ui-design)
  - [**Features in Detail**](#features-in-detail)
  - [**Security \& Data Protection**](#security--data-protection)
  - [**Performance Optimization**](#performance-optimization)
  - [**API \& External Integrations**](#api--external-integrations)
  - [**Error Handling \& Debugging**](#error-handling--debugging)
  - [**Future Enhancements**](#future-enhancements)
  - [**Credits**](#credits)

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
python -m venv venv
venv\Scripts\activate
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Apply Migrations**
```bash
python manage.py migrate
```

### **4. Run the Server**
```bash
python manage.py runserver
```
The app will be available at `http://127.0.0.1:8000/`.

---

## **Database Schema**

## **Stripe Payments**

## **Testing**

## **Deployment**

---

## **UX & UI Design**
- Wireframes & Mockups
- User Stories
- Navigation Structure
- Responsive Design Considerations

## **Features in Detail**
- Guest vs. Authenticated User Features
- Admin Dashboard Features
- Payment Processing Flow
- Order Management System

## **Security & Data Protection**
- Handling Sensitive Information (e.g., Stripe API Keys)
- Preventing CSRF & XSS Attacks
- Using Django Security Middleware
- User Authentication & Password Encryption

## **Performance Optimization**
- Caching Strategies
- Minifying CSS/JS Files
- Database Indexing & Query Optimization
- Image Compression & Lazy Loading

## **API & External Integrations**
- Stripe API for Payments
- Email Service (e.g., SMTP, Mailgun, SendGrid)
- Google Analytics for Traffic Insights

## **Error Handling & Debugging**
- Common Issues & Fixes
- Logging System Setup
- Debugging Django & JavaScript Issues

## **Future Enhancements**
- Wishlist & Favorite Products
- User Reviews & Ratings System
- Discount & Coupon System
- Subscription-Based Pricing Model

---

## **Credits**


```
-- Readme.md
-- Design
-- Dashboard
        --- orders
        --- profiles
--- Testing
        --- UnitTesting