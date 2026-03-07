from app import nui

def pages(route):
    def decorator(func):
        @nui.page(route)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

