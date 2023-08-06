"""
Cryptographer - A Python Cryptography and Hashing Module

Ciphers Included: 
    - Vigenere Cipher (VigenereKey)
    - RSA Cipher (RSAKey)
Hashers Included:
    - Salted Password Hasher (Password)

All of the above ciphers and hashers are combined into one class: 
    - The Cryptographer (Cryptographer)

Setup: 
    >>> from cryptographer import *
"""

from .ciphers.rsa import RSAKey
from .ciphers.vigenere import VigenereKey
from .combinations import combine_ciphers
from .cryptographer import Cryptographer
from .hashers.passwords import Password
from .util import truncate

__all__ = [
    "VigenereKey",
    "RSAKey",
    "Password",
    "Cryptographer",
    "combine_ciphers",
]
