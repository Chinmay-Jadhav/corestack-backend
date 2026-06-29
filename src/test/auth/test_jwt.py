"""
create_access_tokens()

decode_tokens()
"""

import pytest

from src.auth.utils import HashHelper

def test_create_access_token(valid_user_payload) :

    token = HashHelper.create_access_token(user_data=valid_user_payload)

    assert isinstance(token, str)
    assert len(token) > 0

def test_decode_access_token(valid_token, valid_user_payload) :

    decoded = HashHelper.decode_token(valid_token)

    assert decoded is not None

    assert decoded["sub"] == valid_user_payload["uid"]
    assert "jti" in decoded
    assert "exp" in decoded

