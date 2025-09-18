# E-Commerce Site

This is a full-featured e-commerce web application built with **Django** as the backend framework. The project supports user authentication, product browsing, cart management, and secure checkout. Django’s robust ORM and authentication system ensure data integrity and security.

## Features
- User registration, login, and profile management
- Product catalog with filtering by brand, gender, and price
- Shopping cart
- Email verification for new users

## Technology Stack
- **Backend:** Django (Python)
- **Database:** SQLite (default, easily switchable to PostgreSQL or MySQL)
- **Frontend:** HTML, CSS (custom templates)
- **Other:** Django’s built-in authentication, email, and session management

## Getting Started
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```
5. Access the site at [http://localhost:8000/](http://localhost:8000/)
