import sys
from enum import IntEnum

class Status(IntEnum):
    OK = 0
    NO_PROMPT = 1
    INVALID_RESPONSE = 2

# Decorator: Exit automatically if status is not OK
def check_status(func):
    def wrapper(*args, **kwargs):
        status, result = func(*args, **kwargs)
        if status != Status.OK:
            print(f"Error: {status.name}")
            sys.exit(status.value)
        return result
    return wrapper

# Decorator: Optional debug printing
def debug_status(func):
    def wrapper(self, *args, **kwargs):
        if getattr(self, "debug", False):
            print(f"[DEBUG] Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(self, *args, **kwargs)
        if getattr(self, "debug", False):
            print(f"[DEBUG] {func.__name__} returned: {result}")
            print("------------")
        return result
    return wrapper
