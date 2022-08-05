from django.urls import path
from .views import index, CreateDrug

app_name = "payments"
urlpatterns = [
	path("", index.as_view(), name="index"),
	path("add_drugs", CreateDrug.as_view(pk_url_kwarg=0), name="add_drugs")
]