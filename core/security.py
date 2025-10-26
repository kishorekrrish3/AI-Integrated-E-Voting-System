"""
Security Module
Handles cryptographic operations and ID generation
"""

import hashlib
import random
import string
import time

class SecurityManager:
    """Manages security operations: hashing, ID generation, vote integrity"""

    def __init__(self):
        self.hash_algorithm = 'sha256'

    def generate_sha256(self, data):
        """Generate SHA-256 hash of data"""
        return hashlib.sha256(str(data).encode()).hexdigest()

    def generate_voter_id(self):
        """Generate unique voter ID in format: V123ABC456DEF"""
        # Format: V + 3 digits + 3 uppercase letters + 3 digits + 3 uppercase letters
        digits1 = ''.join(random.choices(string.digits, k=3))
        letters1 = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits2 = ''.join(random.choices(string.digits, k=3))
        letters2 = ''.join(random.choices(string.ascii_uppercase, k=3))

        return f"V{digits1}{letters1}{digits2}{letters2}"

    def generate_candidate_id(self):
        """Generate unique candidate ID in format: C + timestamp + random"""
        timestamp = str(int(time.time()))[-6:]
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"C{timestamp}{random_part}"

    def hash_vote(self, voter_id, candidate_id, timestamp):
        """Create tamper-proof vote hash"""
        vote_data = f"{voter_id}:{candidate_id}:{timestamp}"
        return self.generate_sha256(vote_data)

    def verify_vote_integrity(self, voter_id, candidate_id, timestamp, stored_hash):
        """Verify vote hasn't been tampered with"""
        computed_hash = self.hash_vote(voter_id, candidate_id, timestamp)
        return computed_hash == stored_hash

    def hash_password(self, password):
        """Hash password for secure storage"""
        return self.generate_sha256(password)

    def verify_password(self, password, stored_hash):
        """Verify password against stored hash"""
        return self.hash_password(password) == stored_hash

    def generate_session_token(self):
        """Generate random session token"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    def validate_email(self, email):
        """Basic email validation"""
        return '@' in email and '.' in email.split('@')[1]

    def validate_age(self, age):
        """Validate voter age (must be 18+)"""
        try:
            age = int(age)
            return 18 <= age <= 120
        except:
            return False

    def sanitize_input(self, text):
        """Sanitize user input to prevent injection attacks"""
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '{', '}', ';', '\\', '|']
        sanitized = text
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized.strip()
