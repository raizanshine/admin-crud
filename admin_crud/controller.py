from django.conf.urls import url
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse


class AdminController(object):
    model = None
    form_class = None
    fields = '__all__'

    def get_actions(self):
        return {
            'list': self.list,
            'detail': self.detail,
            'create': self.create,
            'update': self.update,
            'delete': self.delete,
        }

    def get_template_names(self, action):
        template_names = {
            'list': 'admin_crud/list.html',
            'detail': 'admin_crud/detail.html',
            'create': 'admin_crud/create.html',
            'update': 'admin_crud/update.html',
            'delete': 'admin_crud/delete.html',
        }

        return template_names[action]

    def get_context_data(self):
        breadcrumbs = [('Home', '/'), (self.model.__name__, None)]
        return {'breadcrumbs': breadcrumbs}

    def get_object(self, pk):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        return obj

    def get_form(self):
        if not self.form_class:
            form_class = modelform_factory(self.model, fields=self.fields)
        else:
            form_class = self.form_class

        return form_class()

    def get_queryset(self):
        return self.model.objects.all()
    
    def list(self, request, *args, **kwargs):
        template = self.get_template_names('list')
        context = self.get_context_data()
        return TemplateResponse(request, template, context)

    def create(self, request, *args, **kwargs):
        template = self.get_template_names('create')
        context = self.get_context_data()
        context['form'] = self.get_form()
        return TemplateResponse(request, template, context)

    def detail(self, request, *args, **kwargs):
        template = self.get_template_names('detail')
        context = self.get_context_data()
        return TemplateResponse(request, template, context)

    def update(self, request, *args, **kwargs):
        template = self.get_template_names('update')
        context = self.get_context_data()
        return TemplateResponse(request, template, context)

    def delete(self, request, *args, **kwargs):
        template = self.get_template_names('delete')
        context = self.get_context_data()
        return TemplateResponse(request, template, context)

    def get_urls(self, **kwargs):
        """
        Generate urls for any available actions
        """
        model_name = self.model.__name__.lower()

        return [
            url(r'^$', self.list, name='%s-list' % model_name),
            url(r'^create/$', self.create, name='%s-create' % model_name),
            url(r'^(?P<pk>\d+)/$', self.detail, name='%s-detail' % model_name),
            url(r'^(?P<pk>\d+)/update/$', self.update, name='%s-update' % model_name),
            url(r'^(?P<pk>\d+)/delete/$', self.delete, name='%s-delete' % model_name),
        ]
