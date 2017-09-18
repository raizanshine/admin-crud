from django.conf.urls import url
from django.forms.models import modelform_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy


class AdminController(object):
    model = None
    form_class = None
    fields = '__all__'

    def get_actions(self):
        return {
            'list': self.list,
            'create': self.create,
            'update': self.update,
            'delete': self.delete,
        }

    def get_template_names(self, action):
        template_names = {
            'list': 'admin_crud/list.html',
            'create': 'admin_crud/create.html',
            'update': 'admin_crud/update.html',
            'delete': 'admin_crud/delete.html',
        }

        return template_names[action]

    def prepare_view(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def get_context_data(self):
        breadcrumbs = [('Home', '/'), (self.model.__name__, None)]
        model_name = self.model.__name__.lower()
        links = {
            'list': reverse_lazy('admin-crud:%s-list' % model_name),
            'create': reverse_lazy('admin-crud:%s-create' % model_name)
        }
        return {
            'breadcrumbs': breadcrumbs,
            'links': links
        }

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj

    def get_form(self, request):
        if not self.form_class:
            form_class = modelform_factory(self.model, fields=self.fields)
        else:
            form_class = self.form_class

        kwargs = {}

        if self.action == 'update':
            kwargs.update({
                'instance': self.get_object()
            })
        if request.method == 'POST':
            kwargs.update({
                'data': request.POST,
                'files': request.FILES,
            })

        return form_class(**kwargs)

    def get_queryset(self):
        return self.model.objects.all()
    
    def list(self, request, *args, **kwargs):
        self.prepare_view(request, *args, **kwargs)
        template = self.get_template_names('list')
        context = self.get_context_data()
        context.update({
            'object_list': self.get_queryset()
        })
        return TemplateResponse(request, template, context)

    def create(self, request, *args, **kwargs):
        self.prepare_view(request, *args, **kwargs)
        template = self.get_template_names('create')
        context = self.get_context_data()
        form = self.get_form(request)
        if request.method == 'POST':
            if form.is_valid():
                obj = form.save()
                return HttpResponseRedirect('/')
        context['form'] = form
        return TemplateResponse(request, template, context)

    def update(self, request, *args, **kwargs):
        self.prepare_view(request, *args, **kwargs)
        self.action = 'update'
        template = self.get_template_names('update')
        context = self.get_context_data()
        form = self.get_form(request)
        if request.method == 'POST':
            if form.is_valid():
                obj = form.save()
                return HttpResponseRedirect('/')
        context['form'] = form
        return TemplateResponse(request, template, context)

    def delete(self, request, *args, **kwargs):
        self.prepare_view(request, *args, **kwargs)
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
            url(r'^(?P<pk>\d+)/$', self.update, name='%s-update' % model_name),
            url(r'^(?P<pk>\d+)/delete/$', self.delete, name='%s-delete' % model_name),
        ]
