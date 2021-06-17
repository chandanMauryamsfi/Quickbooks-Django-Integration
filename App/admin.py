from django.contrib import admin
from App import models

# Register your models here.
admin.site.register(models.Employee)
admin.site.register(models.PrimaryAddr)
admin.site.register(models.Item)
admin.site.register(models.TimeActivity)
admin.site.register(models.Token)
admin.site.register(models.Photo)
