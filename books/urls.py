from django.urls import path
from .views import new_bussiness_month, view_bussiness_month

urlpatterns = [
	path("viewbussinessmonth", view_bussiness_month, name="view_bussiness_month"),
	path("newbussinessmonth", new_bussiness_month, name="new_bussiness_month"),
]