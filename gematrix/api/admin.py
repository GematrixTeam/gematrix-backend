from django.contrib import admin

from api.models import GematrixData, GematrixSource, GematrixDatasets

admin.site.register(GematrixData)
admin.site.register(GematrixSource)
admin.site.register(GematrixDatasets)
