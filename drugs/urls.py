from django.urls import path
from .views import ViewDrugs, add_drugs, sell_drugs, SearchDrugs, tab

app_name= "drugs"
urlpatterns = [
	path('add_drugs', add_drugs, name="add"),
	path('add_drugs/tab', tab, name="tab"),
	path("sell_drugs", sell_drugs, name="sale"),
	path("drugs", ViewDrugs.as_view(), name="view-drugs"),
	path("search", SearchDrugs.as_view(), name="search")
]