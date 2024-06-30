from django.urls import path
from .views import ViewDrugs, ViewStock, SearchDrugs, ViewDrugDetails, SellDrugs, restock, edit, add_drugs, sell_drugs, tab, suspension, injectable

app_name= "drugs"
urlpatterns = [
	path('add_drugs', add_drugs, name="add"),
    path('add_drugs/<int:pk>', restock, name="restock"),
    path('edit/<int:pk>', edit, name="restock"),
	path('add_drugs/tab', tab, name="tab"),
	path('add_drugs/suspension', suspension, name="suspension"),
	path('add_drugs/injectable', injectable, name='injectable'),
	path("sell_drugs", sell_drugs, name="sale"),
    path("<int:pk>/sell", SellDrugs.as_view(), name="sell"),
	path("drugs", ViewDrugs.as_view(), name="view-drugs"),
	path("stock", ViewStock.as_view(), name="view_stock"),
	path("search", SearchDrugs.as_view(), name="search"),
    path("<int:pk>", ViewDrugDetails.as_view(), name="drug"),
]