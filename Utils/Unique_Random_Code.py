import hashlib
import time

class UniqueRandomCodeLib:
    @staticmethod
    def generate_unique_code(prefix: str, counter: int, sender: str) -> str:
        raw = f"{prefix}{counter}{int(time.time())}{sender}"
        hashed = hashlib.sha256(raw.encode()).hexdigest()
        unique_number = int(hashed, 16) % 1_000_000_000
        return f"{prefix}{str(unique_number).zfill(9)}{counter}"