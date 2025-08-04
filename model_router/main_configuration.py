"""Main configuration for services and dependencies."""

import inject
from model_router.domain.user import User
from model_router.storages.user_storage import InMemoryUserStorage
from model_router.services.user_service import UserService
from model_router.services.user_token_service import UserTokenService


def main_configuration(binder: inject.Binder):
    """Configure dependency injection for the main application."""
    
    # Initialize storages
    user_storage = InMemoryUserStorage()
    
    # Initialize services
    user_service = UserService(user_storage)
    user_token_service = UserTokenService()
    
    # Bind services to DI container
    binder.bind_to_constructor(InMemoryUserStorage, lambda: user_storage)
    binder.bind_to_constructor(UserService, lambda: user_service)
    binder.bind_to_constructor(UserTokenService, lambda: user_token_service)


async def initialize_sample_data():
    """Initialize sample data for development/testing."""
    user_storage = inject.instance(InMemoryUserStorage)
    user_token_service = inject.instance(UserTokenService)
    
    # Create sample users
    users = [
        User(email="admin@example.com", additional_info={"role": "admin"}),
        User(email="developer@example.com", additional_info={"role": "developer"}),
        User(email="user@example.com", additional_info={"role": "user"}),
    ]

    saved_users = []
    for user in users:
        saved_user = await user_storage.save(user)
        saved_users.append(saved_user)
    
    # Create sample tokens
    tokens = [
        ("admin-token-123", saved_users[0].uid),  # admin user
        ("dev-token-456", saved_users[1].uid),    # developer user  
        ("user-token-789", saved_users[2].uid),   # regular user
        ("test-key", saved_users[2].uid),         # test token for backward compatibility
    ]
    
    for token, user_uid in tokens:
        user_token_service.add_token(token, user_uid)


@inject.params(user_service=UserService)
def get_user_service(user_service: UserService) -> UserService:
    """Dependency injection for UserService."""
    return user_service


@inject.params(user_token_service=UserTokenService)
def get_user_token_service(user_token_service: UserTokenService) -> UserTokenService:
    """Dependency injection for UserTokenService."""
    return user_token_service


@inject.params(user_storage=InMemoryUserStorage)
def get_user_storage(user_storage: InMemoryUserStorage) -> InMemoryUserStorage:
    """Dependency injection for UserStorage."""
    return user_storage