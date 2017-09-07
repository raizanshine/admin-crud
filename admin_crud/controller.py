from django.conf.urls import url
from django.template.response import TemplateResponse


class AdminController(object):
    model = None

    def get_actions(self):
        return {
            'list': self.list,
        }

    def get_template_name(self, action):
        template_names = {
            'list': 'admin_crud/list.html'
        }

        return template_names[action]

    def get_context_data(self):
        data = {}
        return data
    
    def list(self, request, *args, **kwargs):
        template = self.get_template_name('list')
        context = self.get_context_data()
        return TemplateResponse(request, template, context)

    def get_urls(self, **kwargs):
        """
        Generate urls for any available actions
        """
        return [
            url(r'^$', self.list)
        ]
