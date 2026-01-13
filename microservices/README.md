# Microservices Architecture for Bookshop

This project implements a microservices architecture with 4 independent services:

1. **Customer Service** - Manages customer accounts
2. **Book Service** - Manages book catalog
3. **Cart Service** - Manages shopping carts
4. **API Gateway** - Central entry point

## Services

| Service          | Port | Description         |
| ---------------- | ---- | ------------------- |
| Customer Service | 8001 | Customer management |
| Book Service     | 8002 | Book catalog        |
| Cart Service     | 8003 | Shopping cart       |
| API Gateway      | 8000 | API Gateway         |

## Running Services

```bash
# Customer Service
cd customer_service
python manage.py migrate
python manage.py runserver 8001

# Book Service
cd book_service
python manage.py migrate
python manage.py runserver 8002

# Cart Service
cd cart_service
python manage.py migrate
python manage.py runserver 8003

# API Gateway
cd api_gateway
python manage.py runserver 8000
```

## API Endpoints

All endpoints are accessed through the API Gateway at `http://localhost:8000`

- `/api/customers/` - Customer operations
- `/api/books/` - Book operations
- `/api/carts/` - Cart operations
