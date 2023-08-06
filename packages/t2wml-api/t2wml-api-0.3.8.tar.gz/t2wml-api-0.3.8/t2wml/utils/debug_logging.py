import logging

def basic_debug(func=None):
    def wrapper(*args, **kwargs):
        try:
            function_name = func.__func__.__qualname__
        except:
            function_name = func.__qualname__
        logging.info(f"calling {function_name}")
        try:
            result= func(*args, **kwargs)
            logging.info(f"returned from {function_name}")
            return result
        except Exception as e:
            logging.error(f"{function_name} raised {str(e)}")
            raise e
    return wrapper

def with_args_debug(func=None):
    def wrapper(*args, **kwargs):
        try:
            function_name = func.__func__.__qualname__
        except:
            function_name = func.__qualname__
        logging.info(f"calling {function_name}") 
        logging.debug(f"with args {str(args)} and kwargs {str(kwargs)}")
        try:
            result= func(*args, **kwargs)
            logging.debug(f"{function_name} returned result: {result}")
            return result
        except Exception as e:
            logging.error(f"{function_name} raised {str(e)}")
            raise e
    return wrapper