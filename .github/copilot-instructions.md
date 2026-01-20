# Copilot Instructions: Multi-Architecture Django Bookshop

## Project Overview

This codebase demonstrates **three different architectural patterns** for the same bookshop application (Customer, Book, Cart management). Each implementation is isolated in its own directory with separate Django projects and databases.

### Architecture Implementations

1. **Monolithic** (`monolithic/`) - Traditional Django with ViewSets
   - Single Django app with all models in [shop/models.py](../monolithic/shop/models.py)
   - Uses Django REST Framework ViewSets for CRUD operations
   - Direct ORM access in views

2. **Clean Architecture** (`clean_architecture/`) - Domain-Driven Design
   - **Domain Layer**: Pure Python entities in `domain/entities/` (no Django dependencies)
   - **Application Layer**: Use cases with DTOs in `application/use_cases/`
   - **Infrastructure Layer**: Django ORM adapters implementing repository interfaces
   - **Presentation Layer**: API views that call use cases through dependency injection
   - Key pattern: Views → Use Cases → Repository Interfaces → Django Repositories → ORM Models

3. **Microservices** (`microservices/`) - Service-Oriented with API Gateway
   - 4 independent Django projects: `customer_service`, `book_service`, `cart_service`, `api_gateway`
   - Each service runs on different port (8001, 8002, 8003, 8000)
   - Services communicate via HTTP using service clients (see [service_clients.py](../microservices/cart_service/carts/service_clients.py))
   - API Gateway proxies requests to downstream services (see [proxy.py](../microservices/api_gateway/gateway/proxy.py))

## Critical Architectural Patterns

### Clean Architecture: Entity-Model Separation

- **Domain entities** are dataclasses with business logic (`domain/entities/book.py` has `reduce_stock()` method)
- **ORM models** are Django models for persistence (`infrastructure/persistence/models.py`)
- Repositories convert between entities and models using `_to_entity()` and `_to_model()` methods
- Example: [DjangoBookRepository](../clean_architecture/infrastructure/persistence/repositories.py) converts `BookModel` ↔ `Book` entity

### Dependency Injection in Clean Architecture

- Singleton `Container` class ([container.py](../clean_architecture/infrastructure/container.py)) manages all dependencies
- Views import `container` and call `container.customer_use_cases.create_customer(dto)`
- **Never instantiate use cases or repositories directly in views**

### Microservices: Service Communication

- Cart service validates customer/book existence by calling other services
- Uses `ServiceClient` classes with retry logic and fallback handling
- Service URLs configured in `settings.py` (e.g., `BOOK_SERVICE_URL = 'http://localhost:8002'`)

## Development Workflows

### Running Each Architecture

**Monolithic:**

```bash
cd monolithic
python manage.py migrate
python manage.py runserver 8000
```

**Clean Architecture:**

```bash
cd clean_architecture
python manage.py migrate
python manage.py runserver 8000
```

**Microservices (run in separate terminals):**

```bash
# Terminal 1: Customer Service
cd microservices/customer_service && python manage.py migrate && python manage.py runserver 8001

# Terminal 2: Book Service
cd microservices/book_service && python manage.py migrate && python manage.py runserver 8002

# Terminal 3: Cart Service
cd microservices/cart_service && python manage.py migrate && python manage.py runserver 8003

# Terminal 4: API Gateway
cd microservices/api_gateway && python manage.py runserver 8000
```

### Adding New Features

**Monolithic**: Add model → Add serializer → Add viewset → Register in URLs

**Clean Architecture** (follow this order):

1. Domain entity: Add business logic to `domain/entities/`
2. Repository interface: Define abstract methods in `domain/repositories/interfaces.py`
3. Use case: Implement business flow in `application/use_cases/`
4. Repository implementation: Implement interface in `infrastructure/persistence/repositories.py`
5. View: Call use case through container in `presentation/views.py`
6. Wire up: Add to `Container` if new repository/use case

**Microservices**: Add endpoint to specific service → Update service client if needed → Update API Gateway proxy routes

## Key Conventions

- **UUID Primary Keys**: All models use `CharField(primary_key=True, default=uuid.uuid4)` not auto-increment IDs
- **DTOs in Clean Architecture**: Use dataclasses for input (`CreateBookDTO`) and output to enforce boundaries
- **Entity `to_dict()` Methods**: Entities serialize themselves, not views
- **No Business Logic in Views**: Monolithic views have minimal logic; Clean Architecture views only validate and call use cases
- **Service Client Timeouts**: All inter-service HTTP calls have 5-10 second timeouts

## Database & Dependencies

- Each architecture uses **separate SQLite databases** (`db.sqlite3` in each folder)
- Requirements vary:
  - Monolithic/Microservices: `Django>=4.2`, `djangorestframework>=3.14`
  - Clean Architecture: Adds `dependency-injector>=4.41`
  - Microservices: Adds `requests>=2.31` for service clients

## API Structure

All architectures expose similar REST APIs:

- `/api/customers/` - Customer CRUD
- `/api/books/` - Book CRUD
- `/api/carts/` - Cart operations (`POST /api/carts/{cart_id}/items/` to add items)

**Microservices exception**: All requests go through gateway at `http://localhost:8000`
