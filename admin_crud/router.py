from django.conf.urls import include, url


class Router(object):
    def __init__(self):
        self.registry = []
        self._urls = []

    def register(self, path, Controller):
        self.registry.append([path, Controller])
        controller = Controller()
        self._urls += [
            url(r'^%s/' % path, include(controller.get_urls()))
        ]

    @property
    def urls(self):
        return [self._urls, 'admin', 'admin']
