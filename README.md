**Overview**

This project is a comprehensive e-commerce website developed using Django. It features a user-friendly interface for browsing products, managing a shopping cart, and completing orders. The backend is built with Django, ensuring a robust and scalable application.



**Features**

**Product Catalog**: Browse a wide range of products with detailed descriptions and images.

**Shopping Cart**: Add products to your cart, view quantities, and proceed to checkout.

**Order Management**: Track your orders and view order history.

**User Authentication**: Secure login and registration system for users.

**Admin Panel**: Manage products, orders, and users through a comprehensive admin interface.



**Technologies Used**

**Backend**: Django, Redis

**Database**: SQLite (default for Django)

**Frontend**: HTML, CSS, JavaScript

**Authentication**: Django's built-in authentication system




**Installation**

**Clone the repository:**

git clone https://github.com/sanidhya19/E-Commerce-Website.git
cd E-Commerce-Website


**Set up a virtual environment:**

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


**Install dependencies:**

pip install -r requirements.txt


**Apply migrations:**

python manage.py migrate


**Run the development server:**

python manage.py runserver


Visit http://127.0.0.1:8000/ in your browser to see the website in action.




**Usage**

**User Registration**: Navigate to the registration page to create a new account.

**Product Browsing**: Browse products by category or search for specific items.

**Shopping Cart**: Add products to your cart and proceed to checkout.

**Order Tracking**: View your order history and track the status of current orders.




**Contributing**

Contributions are welcome! To contribute:

Fork the repository.

Create a new branch (git checkout -b feature-name).

Make your changes.

Commit your changes (git commit -am 'Add new feature').

Push to the branch (git push origin feature-name).

Create a new Pull Request.
