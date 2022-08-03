from django.urls import path, include
from .views import newbussinessmonth, viewbussinessmonth

urlpatterns = [
	path("viewbussinessmonth", viewbussinessmonth, name="view_bussinessmonth"),
	path("newbussinessmonth", newbussinessmonth, name="new_bussinessmonth"),
]