# Mechanic Shop API

## Project Description

The Mechanic Shop API is a RESTful backend application built using Flask, SQLAlchemy, Marshmallow, and SQLite.

The API allows users to manage customers, mechanics, service tickets, and inventory items. This phase of the project focused on improving the application through API documentation and automated testing.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- SQLite
- Flask-Limiter
- Flask-Caching
- Flask-Swagger-UI
- Python-JOSE
- Unittest
- Postman
- GitHub

## Features

- Customer CRUD operations
- Mechanic CRUD operations
- Service Ticket management
- Inventory management
- Assign mechanics to service tickets
- Remove mechanics from service tickets
- Add inventory items to service tickets
- Customer login with JWT authentication
- Protected routes
- Rate limiting
- Response caching
- Customer pagination
- Swagger API documentation
- Automated unit testing

## Documentation

Swagger UI was implemented to document all API endpoints, request parameters, response examples, and authentication requirements.

Access Swagger Documentation:

```bash
http://127.0.0.1:5000/api/docs
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/springwilliams26/Mechanic_Shop_API-.git
```

Navigate to Project Directory

```bash
cd Mechanic_Shop_API-
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Virtual Environment

```bash
venv\Scripts\activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Application

```bash
python app.py
```

# Testing

Unit tests were created for:

Customers
Mechanics
Service Tickets
Inventory

Run all tests with:

```bash
python -m unittest discover tests
```

# Author

Spring Williams
