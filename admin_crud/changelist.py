from django.urls import reverse


class ChangeList(object):
    """
    A list of model objects modified for comfy rendering. The class gets controller and queryset and
    then provide only attributes which can be used on object list page.
    """
    def __init__(self, controller, queryset):
        super(ChangeList, self).__init__()
        self.controller = controller
        self.queryset = queryset
        self.model = queryset.model
        self.items = []
        self.titles = []
        self.clickables = ['id']

        fields = controller.fields
        opts = self.model._meta
        if controller.list_fields:
            fields = controller.list_fields
        if fields == '__all__':
            fields = [field.name for field in opts.concrete_fields]

        items = []

        for obj in queryset:
            values = []
            for field in fields:
                values.append({
                    'value': getattr(obj, field),
                    'link': self.get_change_url(obj) if field in self.clickables else False
                })
            items.append(values)
        self.items = items

        for field_name in fields:
            field = opts.get_field(field_name)
            self.titles.append(field.verbose_name)

    def get_change_url(self, obj):
        model_name = self.model.__name__.lower()
        # FIXME: get rid of hardcoding
        return reverse('admin-crud:%s-update' % model_name, args=[obj.pk])
