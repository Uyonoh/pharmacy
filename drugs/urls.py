from django.urls import path
from .views import add_drugs, sell_drugs

urlpatterns = [
	path('add_drugs', add_drugs, name="add"),
	path("sell_drugs", sell_drugs, name="sale"),
]