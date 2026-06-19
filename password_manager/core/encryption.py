import os
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionManager:

    SALT_SIZE = 16
    KEY_ITERATIONS = 100_000

    def __init__(self):
        self._key = None
        self._fernet = None

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.KEY_ITERATIONS,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def set_password(self, password: str, salt: bytes = None) -> bytes:
        if salt is None:
            salt = os.urandom(self.SALT_SIZE)
        self._key = self._derive_key(password, salt)
        self._fernet = Fernet(self._key)
        return salt

    def encrypt(self, data: str) -> bytes:
        if self._fernet is None:
            raise RuntimeError("Encryption key not set. Call set_password() first.")
        return self._fernet.encrypt(data.encode())

    def decrypt(self, token: bytes) -> str:
        if self._fernet is None:
            raise RuntimeError("Encryption key not set. Call set_password() first.")
        return self._fernet.decrypt(token).decode()

    @staticmethod
    def hash_password(password: str) -> str:
        salt = os.urandom(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
        return salt.hex() + ':' + pwd_hash.hex()

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        try:
            salt_hex, hash_hex = stored_hash.split(':')
            salt = bytes.fromhex(salt_hex)
            pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
            return pwd_hash.hex() == hash_hex
        except (ValueError, AttributeError):
            return False
