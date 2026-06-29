import pytest

from src.auth.utils import HashHelper

# HASH HELPER CONFIG
@pytest.fixture
def password_data() :
    """Provide plain pwd and pre-computed hash"""
    plain = "supersecret"
    hashed = HashHelper.hash_password(password=plain)
    return {
        "plain" :plain ,
        "hashed" : hashed
    }


from unittest.mock import MagicMock

from ..auth.dependencies import RoleChecker

# ROLE CHECKER
@pytest.fixture
def admin_checker() :
    """Provides a RoleChecker instance configured for admins"""
    return RoleChecker(['admin'])

@pytest.fixture
def mock_user_factory() :
    """Provides a factory function to create users with specific roles"""
    def _create_user(role : str) :
        return MagicMock(role = role)
    return _create_user


# JWT CHECKER
from src.auth.utils import HashHelper

@pytest.fixture
def valid_user_payload() :
    """Provides a consistent user payload dictionary"""
    return {"uid" : "123"}

@pytest.fixture
def valid_token(valid_user_payload) :
    return HashHelper.create_access_token(user_data=valid_user_payload)