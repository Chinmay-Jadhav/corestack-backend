"""
specifically testing 
class HashHelper :
    hash_password()

    verify_password()
"""

import pytest

from src.auth.utils import HashHelper

def test_password_hashing(password_data) :
    assert password_data["hashed"] != password_data["plain"]


def test_verify_correct_password(password_data) :
    assert HashHelper.verify_password(
        plain_password = password_data["plain"],
        hashed_password= password_data["hashed"]
        )
    
def test_verify_wrong_password(password_data) :
    assert not HashHelper.verify_password(
        plain_password = "wrongpassword",
        hashed_password = password_data["hashed"]
        )