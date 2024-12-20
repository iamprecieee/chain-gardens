from nanoid import generate
from secrets import token_hex


def generate_id():
    """Returns a nanoid string to be used as pk in models"""
    return generate(size=21)


def generate_hex_token():
    """Returns a string to be used as an authentication token"""
    return token_hex(32)
