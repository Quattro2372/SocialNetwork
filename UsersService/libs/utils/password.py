from hashlib import sha256

def encode_password(password: str) -> str:
    return sha256(password.encode('utf-8')).hexdigest()

def check_password(password: str, encoded: str) -> bool:
    return encoded == encode_password(password)