from loguru import logger
from functools import wraps
module_test_count = 0
def log_on_success(func):
    @wraps(func)  # 使用wraps装饰器
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} completed successfully.")
        except Exception as e:
            logger.error(f"{func.__name__} failed with error: {e}")
            raise
        return result
    return wrapper
def count_function(func):

    global module_test_count
    @wraps(func)  # 使用wraps装饰器
    def wrapper(self, *args, **kwargs):
        global module_test_count
        module_test_count += 1
        return func(self, *args, **kwargs)
    return wrapper