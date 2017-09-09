from django.apps import apps as dj_apps
from django.conf.urls import include, url
from django.template.response import TemplateResponse
from django.utils.text import capfirst


class Router(object):
    def __init__(self):
        self.registry = []
        self._urls = [
            url(r'^$', self.index_view, name='index')
        ]

    def build_groups(self, request):
        apps = self.registry
        models = {}

        for path, controller in apps:
            app_label = controller.model._meta.app_label
            if app_label not in models:
                models[app_label] = {
                    'verbose_name': dj_apps.get_app_config(app_label).verbose_name,
                    'admins': []
                }
            controller_info = {
                'verbose_name': capfirst(controller.model._meta.verbose_name_plural),
            }
            models[app_label]['admins'].append(controller_info)
        return models

    def index_view(self, request, *args, **kwargs):
        groups = self.build_groups(request)
        return TemplateResponse(
            request,
            template='admin_crud/index.html',
            context={
                'groups': groups
            }
        )

    def register(self, path, Controller):
        controller = Controller()
        self.registry.append([path, controller])
        self._urls += [
            url(r'^%s/' % path, include(controller.get_urls()))
        ]

    @property
    def urls(self):
        return [self._urls, 'admin-crud', 'admin-crud']
