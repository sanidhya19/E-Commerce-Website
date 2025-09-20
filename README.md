# E-Commerce Website

## Overview

This **E-Commerce Website** is a full-featured web application built using Django.  
It allows users to browse products, manage a shopping cart, and complete orders seamlessly.  
The application also includes an admin panel for managing products, orders, and users.

---

## Features

- **Product Catalog:** Browse a wide range of products with detailed descriptions and images.  
- **Shopping Cart:** Add products to your cart, view quantities, and proceed to checkout.  
- **Order Management:** Track orders and view order history.  
- **User Authentication:** Secure login and registration system.  
- **Admin Panel:** Manage products, orders, and users easily through the admin interface.

---

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python, Django  
- **Database:** SQLite (default for Django)  
- **Authentication:** Django's built-in authentication system

---

## Installation

### Prerequisites

- Python 3.x  
- pip (Python package installer)  
- git  

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/sanidhya19/E-Commerce-Website.git
cd E-Commerce-Website
```


2. **Set up a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. **Apply migrations:**

```bash
python manage.py migrate
```

4. **Run the development server:**

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser to see the website in action.

---


## Usage

- **User Registration**: Navigate to the registration page to create a new account.
- **Product Browsing**: Browse products by category or search for specific items.
- **Shopping Cart**: Add products to your cart and proceed to checkout.
- **Order Tracking**: View your order history and track the status of current orders.




## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.

2. Create a new branch 

```bash
git checkout -b feature-name
```

3. Make your changes.

4. Commit your changes 

```bash
git commit -am 'Add new feature'
```

5. Push to the branch 

```bash
git push origin feature-name
```

6. Create a new Pull Request.
