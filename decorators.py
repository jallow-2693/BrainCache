import functools
import json
from .core import BrainCache

_default_cache = BrainCache()

def cache(ttl=60):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Clé de cache robuste
            try:
                key = f"{func.__name__}:{args}:{json.dumps(kwargs, sort_keys=True)}"
            except TypeError:
                key = f"{func.__name__}:{args}:{str(kwargs)}"
            result = _default_cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                _default_cache.set(key, result, ttl=ttl)
            return result
        return wrapper
    return decorator
