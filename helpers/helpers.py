

def python_way_wrapper(func_to_wrap):
    def wrapper(*args, **kwargs):
        try:
            res = func_to_wrap(*args, **kwargs)
        except Exception as e:
            print(f"Exception occurred during {func_to_wrap.__name__}")
            res = None
        return res
    return wrapper
