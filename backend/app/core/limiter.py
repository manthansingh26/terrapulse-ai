"""
Shared rate-limiter instance.
Import this in main.py AND in endpoint files.
Never import from app.main in endpoint files — that causes circular imports.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
