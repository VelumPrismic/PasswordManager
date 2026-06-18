import re


class StrengthChecker:
    """Evaluate password strength based on entropy and patterns."""

    COMMON_PASSWORDS = {
        'password', '123456', '12345678', 'qwerty', 'abc123',
        'monkey', 'master', 'dragon', 'login', 'princess',
        'football', 'shadow', 'sunshine', 'trustno1', 'iloveyou',
        'batman', 'access', 'hello', 'charlie', 'password1'
    }

    def check(self, password: str) -> dict:
        """
        Check password strength.
        Returns dict with score (0-100), label, and details.
        """
        if not password:
            return {
                'score': 0,
                'label': 'Empty',
                'color': '#45475a',
                'details': ['Enter a password to check']
            }

        score = 0
        details = []

        # Length scoring (up to 30 points)
        length = len(password)
        if length >= 16:
            score += 30
            details.append(f'Length: {length} chars (excellent)')
        elif length >= 12:
            score += 25
            details.append(f'Length: {length} chars (good)')
        elif length >= 8:
            score += 15
            details.append(f'Length: {length} chars (fair)')
        elif length >= 6:
            score += 5
            details.append(f'Length: {length} chars (short)')
        else:
            details.append(f'Length: {length} chars (too short)')

        # Character diversity (up to 40 points)
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_symbol = bool(re.search(r'[^A-Za-z0-9]', password))

        diversity = sum([has_upper, has_lower, has_digit, has_symbol])
        score += diversity * 10

        if has_upper:
            details.append('Has uppercase letters')
        if has_lower:
            details.append('Has lowercase letters')
        if has_digit:
            details.append('Has numbers')
        if has_symbol:
            details.append('Has special characters')

        # Pattern penalties (up to -30 points)
        # Common password check
        if password.lower() in self.COMMON_PASSWORDS:
            score -= 40
            details.append('WARNING: Common password detected!')

        # Sequential characters (e.g., abc, 123)
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
            score -= 10
            details.append('Contains sequential letters')

        if re.search(r'(012|123|234|345|456|567|678|789)', password):
            score -= 10
            details.append('Contains sequential numbers')

        # Repeated characters
        if re.search(r'(.)\1{2,}', password):
            score -= 10
            details.append('Contains repeated characters')

        # All same character type
        if re.fullmatch(r'[A-Z]+', password) or re.fullmatch(r'[a-z]+', password) or re.fullmatch(r'\d+', password):
            score -= 15
            details.append('Only uses one character type')

        # Entropy bonus (up to 30 points)
        charset_size = 0
        if has_upper:
            charset_size += 26
        if has_lower:
            charset_size += 26
        if has_digit:
            charset_size += 10
        if has_symbol:
            charset_size += 32

        if charset_size > 0:
            import math
            entropy = length * math.log2(charset_size)
            entropy_bonus = min(30, int(entropy / 10))
            score += entropy_bonus
            details.append(f'Entropy: {entropy:.1f} bits')

        # Clamp score to 0-100
        score = max(0, min(100, score))

        # Determine label and color
        if score >= 80:
            label = 'Very Strong'
            color = '#a6e3a1'  # Green
        elif score >= 60:
            label = 'Strong'
            color = '#94e2d5'  # Teal
        elif score >= 40:
            label = 'Fair'
            color = '#f9e2af'  # Yellow
        elif score >= 20:
            label = 'Weak'
            color = '#fab387'  # Orange
        else:
            label = 'Very Weak'
            color = '#f38ba8'  # Red

        return {
            'score': score,
            'label': label,
            'color': color,
            'details': details
        }
