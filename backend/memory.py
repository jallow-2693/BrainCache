class MemoryBackend:
    def __init__(self):
        self.cache = {}

    def set(self, key, value, expire_at=None):
        self.cache[key] = (value, expire_at)

    def get(self, key):
        return self.cache.get(key, None)

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache.clear()
