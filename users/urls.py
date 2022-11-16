from django.urls import path, include
from .views import register, success, new_form

app_name = "users"
urlpatterns = [
	path("register/", register, name="register"),
	path("succsess/", success, name="success"),
	path("new/", new_form),
	path("", include("django.contrib.auth.urls"))
]