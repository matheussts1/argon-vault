from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
lm = LoginManager()
ph = PasswordHasher(hash_len=32, time_cost=3, memory_cost=65536, parallelism=4)
limiter = Limiter(key_func=get_remote_address)

csp = (
    "default-src 'self'; "
    "style-src 'self' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
    "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
    "script-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com 'wasm-unsafe-eval'; " 
    "worker-src 'self'; "
    "img-src 'self' data:; "
)