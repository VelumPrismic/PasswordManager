import secrets
import string


class PasswordGenerator:
    """Generate secure random passwords."""

    def __init__(self):
        self.uppercase = True
        self.lowercase = True
        self.numbers = True
        self.symbols = True
        self.length = 16

    def generate(self) -> str:
        """Generate a password based on current settings."""
        charset = ""
        required_chars = []

        if self.uppercase:
            charset += string.ascii_uppercase
            required_chars.append(secrets.choice(string.ascii_uppercase))

        if self.lowercase:
            charset += string.ascii_lowercase
            required_chars.append(secrets.choice(string.ascii_lowercase))

        if self.numbers:
            charset += string.digits
            required_chars.append(secrets.choice(string.digits))

        if self.symbols:
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            charset += symbols
            required_chars.append(secrets.choice(symbols))

        if not charset:
            charset = string.ascii_lowercase
            required_chars = [secrets.choice(charset)]

        remaining_length = self.length - len(required_chars)
        password_chars = required_chars + [secrets.choice(charset) for _ in range(remaining_length)]

        password_list = list(password_chars)
        secrets.SystemRandom().shuffle(password_list)

        return ''.join(password_list)

    def set_options(self, length: int = 16, uppercase: bool = True,
                    lowercase: bool = True, numbers: bool = True,
                    symbols: bool = True):
        """Set generation options."""
        self.length = max(8, min(64, length))
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.numbers = numbers
        self.symbols = symbols
