from django.contrib import admin
from web_models import models
# Register your models here.
admin.site.register(models.Items)
admin.site.register(models.Services)
admin.site.register(models.ServiceType)
admin.site.register(models.Templates)
admin.site.register(models.Trigger)
admin.site.register(models.Host)
admin.site.register(models.HostGroup)
admin.site.register(models.MonitorGroup)
admin.site.register(models.UserInfo)
admin.site.register(models.Admin)
