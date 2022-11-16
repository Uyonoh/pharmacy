from django.contrib import admin

from drugs.models import Drug, Sale

# Register your models here.
admin.site.register(Drug)
admin.site.register(Sale)