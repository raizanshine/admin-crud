from django.conf.urls import url
from django.template.response import TemplateResponse


class AdminController(object):
    model = None

    def get_actions(self):
        return {
            'list': self.list,
            'detail': self.detail,
            'create': self.create,
        }

    def get_template_names(self, action):
        template_names = {
            'list': 'admin_crud/list.html',
            'detail': 'admin_crud/detail.html',
            'create': 'admin_crud/create.html',
        }

        return template_names[action]

    def get_context_data(self):
        data = {}
        return data
    
    def list(self, request, *args, **kwargs):
        template = self.get_template_names('list')
        context = self.get_context_data()
        return TemplateResponse(request, template, context)

    def create(self, request, *args, **kwargs):
        template = self.get_template_names('create')
        context = self.get_context_data()
        return TemplateResponse(request, template, context)

    def detail(self, request, *args, **kwargs):
        template = self.get_template_names('detail')
        context = self.get_context_data()
        return TemplateResponse(request, template, context)

    def get_urls(self, **kwargs):
        """
        Generate urls for any available actions
        """
        return [
            url(r'^$', self.list),
            url(r'^create/$', self.create),
            url(r'^(?<pk>\d+)/$', self.detail),
        ]
