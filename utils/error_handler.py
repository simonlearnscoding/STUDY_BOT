import asyncio
import functools
import traceback

def error_handler(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            exc_info = traceback.format_exc()  # Get the traceback information
            print(f"An error occurred in {func.__name__}: {e}\n{exc_info}")
            # Optionally re-raise the exception
            raise
    return wrapper

def class_error_handler(cls):
    for name, method in cls.__dict__.items():
        if asyncio.iscoroutinefunction(method) and not name.startswith('__'):
            setattr(cls, name, error_handler(method))
    return cls
