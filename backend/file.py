import json
import time
import os
from threading import Lock

class FileBackend:
    def __init__(self, filepath='braincache.json'):
        self.filepath = filepath
        self.lock = Lock()
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                try:
                    self.cache = json.load(f)
                except json.JSONDecodeError:
                    self.cache = {}
        else:
            self.cache = {}

    def _save(self):
        with self.lock:
            with open(self.filepath, 'w') as f:
                json.dump(self.cache, f, indent=2)

    def set(self, key, value, expire_at=None):
        try:
            json.dumps(value)  # Test si la valeur est sérialisable
        except TypeError:
            raise ValueError("La valeur à stocker doit être JSON-serializable")
        with self.lock:
            self.cache[key] = {
                'value': value,
                'expire_at': expire_at
            }
            self._save()

    def get(self, key):
        entry = self.cache.get(key)
        if entry:
            if entry['expire_at'] is None or entry['expire_at'] > time.time():
                return (entry['value'], entry['expire_at'])
            else:
                self.delete(key)
        return None

    def delete(self, key):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                self._save()

    def clear(self):
        with self.lock:
            self.cache.clear()
            self._save()
