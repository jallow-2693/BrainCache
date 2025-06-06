import threading
import time

class CacheCleaner(threading.Thread):
    def __init__(self, cache, interval=60):
        super().__init__(daemon=True)
        self.cache = cache
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            time.sleep(self.interval)
            keys = list(self.cache.backend.cache.keys())
            for key in keys:
                self.cache.get(key)  # cela déclenche la suppression si expiré

    def stop(self):
        self.running = False
