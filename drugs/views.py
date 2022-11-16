from datetime import date
from xmlrpc.client import Boolean
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
#from requests import request
from books.models import Credit, Debit, Stock
from .forms import DrugForm, SaleForm
from .models import Drug, Sale

# Create your views here.

class index(FormView):
	template_name = "add_drugs.html"
	form_class = DrugForm
	success_url = "add_drugs"

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)


def update_stock_(drug, form):
	form.instance.id = drug.id
	new_stock_amount = form.instance.purchase_amount
	no_tabs, no_cards = form.instance.tab_cd.split("/")
	no_tabs, no_cards = int(no_tabs), int(no_cards)

	update_amount = new_stock_amount * no_tabs * no_cards
	form.instance.stock_amount = drug.stock_amount + update_amount
	form.instance.day_added = str(date.today())


def add_drugs(request):
	if request.method =="POST":
		form = DrugForm(request.POST)
		
		# If the data is valid check if the drug with the same name, weight and exp_date exists
		# If not save the drug and register debit, else update existing drug
		if form.is_valid():
			drug = Drug.objects.filter(drug_name=form.instance.drug_name.upper(), weight=form.instance.weight, exp_date=form.instance.exp_date)
			# print(form.fields['drug_name'])
			price = form.instance.price
			if not drug.count():
				
				form.save()
				debit_stock(form.instance)
			else:
				drug = drug[0]
				#form.instance.id = drug.id
				#form.instance.stock_amount += drug.stock_amount

				update_stock_(drug, form)

				form.save(first_stock=False)
				debit_stock(drug, price=price)
			form = DrugForm()				
		else:
			err_msg = f"Oops! Invalid form: {form.errors.as_text()}"
		
	else:
		form = DrugForm()
	return render(request, "drugs/add_drugs.html", {"form":form})


# Dispay price as drugs are selected for sale

def sell_drugs(request):
	print(request.user.is_authenticated)
	if request.method == "POST":
		print(request.POST)
		form = SaleForm(request.POST)
		err_msg = ""

		#If the data is valid check if the drug exists
		# If so subtract from drug and register sales and credit
		if form.is_valid():
			drug = Drug.objects.filter(drug_name=form.instance.drug_name.upper(), weight=form.instance.weight)
			if drug.count():
				drug = drug[0]
				form.instance.drug = drug
				if request.POST.get("add_sale_list"):
					form.add(drug)
					#print("list")
				elif request.POST.get("register_sale"):
					is_tab = False
					if request.POST.get("tab-check"):
						is_tab = True
					try:
						form.add(drug, is_tab, register=True)
						credit(form.instance, is_tab)
					except ValueError:
						if drug.out_of_stock == True:
							err_msg = f"{drug.drug_name} is not available at the moment!"
						else:
							err_msg = "The amount sold is more than available.\nPlease try again!"
					form = SaleForm()
					
					print("reg!")
				#return HttpResponseRedirect("./sell_drugs", {"form": form})
				
			else:
				err_msg = "Drug not found!"
		return render(request, "drugs/sell_drugs.html", {"form":form, "err_msg":err_msg})
	else:
		form = SaleForm()
		return render(request, "drugs/sell_drugs.html", {"form":form})


def debit_stock(drug, price=0):
	"""add drug to stock and register debit"""
	_debit = Debit()
	_stock = Stock()

	_debit.item = str(drug)
	_drug_no_tabs = int(drug.get_tab_cd()[0])
	_debit.amount = price
	_debit.save()

	_stock.drug = str(drug)
	_stock.price = price
	_stock.save()

def credit(drug, is_tab: Boolean):
	"""register credit"""
	_credit = Credit()
	_credit.item = str(drug)
	_credit.amount = drug.compute(is_tab)
	_credit.save()


def view_drugs(request):
	drugs = {}

	return render(request, "drugs/drugs.html", {"drugs":drugs})

class ViewDrugs(ListView):
	model = Drug
	template_name = "drugs/drugs.html"
	context_object_name = "drugs"
	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["d-class"] = "exp-far"
		context["headings"] = ["drug_name", "brand_name", "drug_type", "weight",
							"manufacturer", "exp_date", "stock_amount", "price", "category",
							"purpose", "location"]
		print(context)
		return context
	


class SearchDrugs(ViewDrugs):
	#query = request["POST"]
	model = Drug
	

	def search(self, request):
		key = request.GET["search-box"].upper()
		queryset = Drug.objects.filter(drug_name=key)
		if not queryset:
			queryset = Drug.objects.filter(brand_name=key)
		
		return queryset
	
	
	# queryset = search(request)
	def get(self, request):
		self.queryset = self.search(request)
		return super().get(request)

	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
	
	