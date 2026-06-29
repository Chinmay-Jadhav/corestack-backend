import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status

from ...auth.dependencies import RoleChecker

    

def test_role_checker_allows_valid_role(admin_checker, mock_user_factory) :

    user = mock_user_factory(role = "admin")

    assert admin_checker(user) is True


def test_role_checker_denies_invalid_role(admin_checker, mock_user_factory) :

    user = mock_user_factory(role = "user")

    with pytest.raises(HTTPException) as exc_info :
        admin_checker(user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You don't have permission to access this resource"