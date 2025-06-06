import time
from .backend.memory import MemoryBackend

class BrainCache:
    def __init__(self, backend=None):
        self.backend = backend or MemoryBackend()

    def set(self, key, value, ttl=None):
        expire_at = time.time() + ttl if ttl else None
        self.backend.set(key, value, expire_at)

    def get(self, key):
        entry = self.backend.get(key)
        if entry:
            value, expire_at = entry
            if not expire_at or expire_at > time.time():
                return value
            else:
                self.delete(key)
        return None

    def has(self, key):
        return self.get(key) is not None

    def delete(self, key):
        self.backend.delete(key)

    def clear(self):
        self.backend.clear()
