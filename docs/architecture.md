Code Architecture

Domain-Driven Design (DDD) Pattern:

- Clear separation between domain/, services/, storages/, and api/ layers
- Domain entities inherit from BaseEntity with KSUID generation and timestamps
- Business logic encapsulated in service classes

Dependency Injection:

- Heavy use of inject library for dependency management
- Constructor-based injection with explicit parameter declarations
- Centralized configuration in configuration.py with binder.bind_to_constructor()

Storage Pattern:

- Abstract storage interfaces with multiple implementations (PostgreSQL, In-Memory, Redis)
- SQLAlchemy imperative mapping with Table definitions
- Consistent async/await patterns throughout

Code Style

Async-First Architecture:

- All storage and service methods are async
- Proper use of asyncio.to_thread() for blocking operations (YooKassa, Kucoin)
- FastAPI for async HTTP handling

Error Handling:

- Custom domain exceptions (EntityNotFound, StateError)
- Comprehensive try-catch blocks with proper logging
- Error state tracking in transaction entities

Type Hints:

- Extensive use of type annotations
- Optional types for nullable fields
- Pydantic models for data validation

Logging:

- Structured logging with CallContext for traceability
- Consistent log messages with context information
- System call contexts for background processes

Preferred Patterns

Service Layer:
class TxService:
def __init__(self, storage: Storage, adapter: Adapter, ...):
self._storage = storage
self._adapter = adapter

- Private attributes with underscore prefix
- Single responsibility per service
- Clear method naming (process_waiting_fiat_tx, withdraw_asset)

State Management:

- Explicit status transitions with set_status() method
- Previous status tracking for audit trails
- Status-based workflow processing

Adapter Pattern:

- External service integrations (YooKassa, Kucoin) wrapped in adapters
- Abstract base classes with concrete implementations
- Mock implementations for testing

Data Modeling:

- Pydantic for domain models with validation
- Clear field naming (amount_buy, amount_sell vs generic amount)
- Optional fields properly typed with Optional[T]

Architecture Strengths

1. Separation of Concerns: Clear boundaries between layers
2. Testability: In-memory storage implementations for testing
3. Extensibility: Abstract interfaces allow easy swapping of implementations
4. Observability: Comprehensive logging and error tracking
5. Type Safety: Strong typing throughout the codebase
6. Async Performance: Non-blocking operations for external services

Notable Conventions

- File Organization: Feature-based organization within layers
- Naming: Snake_case for variables/functions, PascalCase for classes
- Comments: Minimal comments, self-documenting code preferred
- Error Tracking: Errors stored in entity fields for persistence
- Transaction Processing: Single-transaction methods for better composability

The architecture demonstrates a mature, production-ready Python service with proper abstraction layers, comprehensive
error handling, and
scalable async patterns.