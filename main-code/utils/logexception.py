import logging

logging.basicConfig(
    filename='exceptions.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def log_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"exception occurred in {func.__name__}: {str(e)}",
                          exc_info=True)
            raise
        return wrapper
