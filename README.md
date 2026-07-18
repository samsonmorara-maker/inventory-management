# Inventory Management System 

## Project Description

This project is a Flask-based REST API for managing inventory items for a small retail company.

The application allows employees to:

- View inventory products
- Add new inventory items
- Update product prices and stock levels
- Delete products
- Search product information using the OpenFoodFacts API

The application uses a temporary in-memory array as simulated data storage and integrates with OpenFoodFacts to retrieve additional product details using a barcode.


# Technologies Used

- Python 3
- Flask
- Requests
- Pytest
- OpenFoodFacts API

# Installation Instructions

## 1. Clone the repository

git clone <your-github-repository-url>

cd inventory-management
## 2. Create Environment
- pipenv install
- pipenv shell
## 3.Running application
- flask run
- and in another terminal python cli.py
## Author
developed by Samson Manoti