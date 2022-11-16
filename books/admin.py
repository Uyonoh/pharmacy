from django.contrib import admin

from books.models import BussinessMonth, Credit, Debit, Stock

# Register your models here.
admin.site.register(BussinessMonth)
admin.site.register(Credit)
admin.site.register(Debit)
admin.site.register(Stock)