import unittest
from jose import jwt, JWTError

from app.auth import create_access_token, hash_password, verify_password
from app.config import JWT_ALGORITHM, get_jwt_secret


class TestAuth(unittest.TestCase):
    """Unit tests for password hashing and JWT token operations."""

    def test_hash_password_produces_bcrypt_hash(self):
        password = "SecurePassword123!"
        hashed = hash_password(password)
        self.assertNotEqual(password, hashed)
        self.assertTrue(hashed.startswith("$2b$") or hashed.startswith("$2a$"))

    def test_verify_password_correct(self):
        password = "MySecretPassword456"
        hashed = hash_password(password)
        self.assertTrue(verify_password(password, hashed))

    def test_verify_password_incorrect(self):
        password = "CorrectPassword789"
        hashed = hash_password(password)
        self.assertFalse(verify_password("WrongPassword", hashed))

    def test_create_and_decode_access_token(self):
        user_id = 123
        token = create_access_token(user_id=user_id)
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)

        # Decode token and verify claims
        payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        self.assertEqual(payload.get("sub"), str(user_id))
        self.assertIn("exp", payload)

    def test_decode_invalid_token_raises_jwt_error(self):
        with self.assertRaises(JWTError):
            jwt.decode("invalid.token.string", get_jwt_secret(), algorithms=[JWT_ALGORITHM])


if __name__ == "__main__":
    unittest.main()

