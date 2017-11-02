def action(url):
    def decorator(func):
        func.url = url
        func.action = True
        return func

    return decorator
