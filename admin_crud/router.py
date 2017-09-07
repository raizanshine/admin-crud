class Router(object):
    def __init__(self):
        self.registry = []
        self._urls = []

    def register(self, path, controller):
        self.registry.append([path, controller])
        self._urls += controller.get_urls()

    @property
    def urls(self):
        return self._urls
