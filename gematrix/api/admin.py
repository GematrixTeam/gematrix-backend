from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from api.models import DataPoint, Producer, Dataset


class DataPointInline(admin.TabularInline):

    model = DataPoint
    fk_name = 'related_obj'
    fields = ('x_data', 'y_value')
    extra = 0


@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):

    list_display = ('x_data', 'y_value', 'related_obj')
    fields = ('x_data', 'y_value')

    def get_model_name(self, obj):
        return getattr(getattr(obj, 'related_obj', None), 'title', None) or ''
    get_model_name.short_description = _('Связанный объект')


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):

    fields = ('title', 'source_url')
    list_display = ('title', 'source_url')


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):

    list_display = ('title', 'created', 'updated', 'source')
    fields = ('title', 'created', 'updated', 'source')
    readonly_fields = ['created', 'updated']
    inlines = (DataPointInline,)
