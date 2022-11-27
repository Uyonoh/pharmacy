from django.contrib import admin

from drugs.models import Drug, Sale, Tablet

# Register your models here.
admin.site.register(Drug)
admin.site.register(Sale)
admin.site.register(Tablet)