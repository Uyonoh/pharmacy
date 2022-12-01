from django.contrib import admin

from drugs.models import Drug, Sale, Tablet, Suspension, Injectable

# Register your models here.
admin.site.register(Drug)
admin.site.register(Sale)
admin.site.register(Tablet)
admin.site.register(Suspension)
admin.site.register(Injectable)