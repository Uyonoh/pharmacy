from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import FormView, CreateView
from drugs.models import Drug
from drugs.forms import DrugForm

# Create your views here.

class CreateDrug(CreateView):
	model = Drug
	fields = ["drug_name", "brand_name", "drug_type", "weight",
		"manufacturer", "exp_date", "stock_amount", "price", "category",
		"purpose", "location"]
	template_name = "drugs/add_drugs.html"
	#success_url = "add_drugs"

	def form_valid(self, request, form):
		print(self.success_url)
		return render( self.template_name, {"form": self})

	def get_object(self, request, queryset):
		if queryset is None:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, drug_name=request.POST["drug_name"], weight=request.POST["weight"], exp_date=request.POST["exp_date"])

	def post(self, request, *args, **kwargs):
		# for drug in self.queryset:
		# 	self.queryset[i] 
		# obj = self.queryset[0]
		# self.queryset = self.get_queryset()
		# drug = self.queryset.filter(drug_name=request.POST["drug_name"], weight=request.POST["weight"], exp_date=request.POST["exp_date"])
		# pk = drug[0]
		if self.get_object(request, self.queryset):
			self.object = self.get_object( request, self.queryset)
			print("III")
		return super().post(request, *args, **kwargs)
		

class index(FormView):
	template_name = "drugs/add_drugs.html"
	form_class = DrugForm
	success_url = "add_drugs"

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)