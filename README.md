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