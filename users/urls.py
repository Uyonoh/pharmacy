from django.urls import path
from .views import register, success

app_name = "users"
urlpatterns = [
	path("register", register, name="register"),
	path("succsess", success, name="success"),
]