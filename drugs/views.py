from datetime import date
import re
from typing import Any
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse
from books.models import Credit, Debit, Stock
from .forms import DrugForm, SaleForm, SalesForm, TabletForm, SuspensionForm, InjectableForm
from .models import Drug, Sale, Tablet, Suspension, Injectable
# Create your views here.

class index(FormView):
	template_name = "add_drugs.html"
	form_class = DrugForm
	success_url = "add_drugs"

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

def dict_drug(drug):
	drug_ = {}
	drug_["drug_name"] = drug.drug_name
	drug_["brand_name"] = drug.brand_name
	drug_["drug_type"] = drug.drug_type
	drug_["state"] = drug.state
	drug_["weight"] = drug.weight
	drug_["manufacturer"] = drug.manufacturer
	drug_["exp_date"] = str(drug.exp_date)
	drug_["stock_amount"] = drug.stock_amount
	drug_["purchase_amount"] = drug.purchase_amount
	drug_["units"] = drug.units
	drug_["price"] = drug.price
	drug_["cost_price"] = drug.cost_price
	drug_["category"] = drug.category
	drug_["purpose"] = drug.purpose
	drug_["location"] = drug.location
	drug_["day_added"] = drug.day_added

	return drug_

def make_drug(drug):
	drug_ = Drug()
	
	drug_.drug_name = drug["drug_name"]       
	drug_.brand_name = drug["brand_name"]      
	drug_.drug_type = drug["drug_type"]       
	drug_.state = drug["state"]           
	drug_.weight = drug["weight"]          
	drug_.manufacturer = drug["manufacturer"]    
	drug_.exp_date = drug["exp_date"]        
	drug_.stock_amount = drug["stock_amount"]    
	drug_.purchase_amount = drug["purchase_amount"]
	drug_.units = drug["units"]  
	drug_.price = drug["price"]         
	drug_.cost_price = drug["cost_price"]           
	drug_.category = drug["category"]        
	drug_.purpose = drug["purpose"]         
	drug_.location = drug["location"]        
	drug_.day_added = drug["day_added"]       

	if not drug_.stock_amount:
		drug_.stock_amount = 0
	return drug_

def tab(request):
	drug = make_drug(request.session["drug"])
	if request.method =="POST":
		form = TabletForm(request.POST)

		if form.is_valid():
			form.instance.drug = drug
			drug.save()
			form.save()
			print(form)
			add_stock(drug, request.session["purchase_price"])
			
			return HttpResponseRedirect(reverse("drugs:add"))
			
	else:
		form = TabletForm()
	return render(request, "drugs/add_drugs.html", {"form":form})

def suspension(request):
	drug = make_drug(request.session["drug"])
	if request.method == "POST":
		form = SuspensionForm(request.POST)

		if form.is_valid():
			form.instance.drug = drug
			drug.save()
			form.save()
			add_stock(drug, request.session["purchase_price"])

			return HttpResponseRedirect(reverse("drugs:add"))

	else:
		form = SuspensionForm()
	return render(request, "drugs/add_drugs.html", {"form":form})

def injectable(request):
	drug = make_drug(request.session["drug"])
	if request.method == "POST":
		form = InjectableForm(request.POST)

		if form.is_valid():
			form.instance.drug = drug
			drug.save()
			form.save()
			add_stock(drug, request.session["purchase_price"])

			return HttpResponseRedirect(reverse("drugs:add"))

		else:
			form = InjectableForm()
		return render(request, "drugs/add_drugs.html", {"form":form})

def update_stock_tab(drug, form):
	new_stock_amount = form.instance.purchase_amount
	tablet = drug.tablet_set.all()[0]
	no_tabs, no_cards = tablet.tab_cd.split("/")
	no_tabs, no_cards = int(no_tabs), int(no_cards)

	update_amount = new_stock_amount * no_tabs * no_cards
	drug.puchase_amount = new_stock_amount 					# Just because I can!!!
	drug.stock_amount = drug.stock_amount + update_amount
	drug.day_added = str(date.today())

	tablet.set_price
	drug.save()

def update_stock(form, drug, price):
	if form.instance.state == "Tab":
		drug.tablet_set.all()[0].update_stock(form.instance.purchase_amount, form.instance.units, price)
		# update_stock_tab(drug, form)
	elif form.instance.state == "Suspension":
		drug.suspension_set.all()[0].update_stock(form.instance.purchase_amount, form.instance.units, price)
	
	else:
		drug.injectable_set.all()[0].update_stock(form.instance.purchase_amount, form.instance.units, price)

def add_drugs(request):
	if request.method =="POST":
		form = DrugForm(request.POST)
		
		# If the data is valid check if the drug with the same name, weight and exp_date exists
		# If not save the drug and register debit, else update existing drug
		# print(form)
		# print(hasattr(form, "brand_name"))
		# for i in form._bound_items(): print(i)
	
		if form.is_valid():
			
			# form.upper()
			# drug = Drug.objects.filter(drug_name=form.instance.drug_name, weight=form.instance.weight, exp_date=form.instance.exp_date)

			drug = Drug.objects.filter(drug_name=form.instance.drug_name.upper(), weight=form.instance.weight, exp_date=form.instance.exp_date, manufacturer=form.instance.manufacturer)
			# print(form.fields['drug_name'])
			
			cost_price = float(request.POST.get("cost_price"))
			price = float(request.POST.get("sale_price"))
			print(price)

			
			if not drug.count():
				form.upper()
				request.session["drug"] = dict_drug(form.instance)
				request.session["drug"]["cost_price"] = cost_price
				request.session["drug"]["price"] = price
				request.session["purchase_price"] = cost_price
				# form.save()
				# print(form)
				if form.instance.state == "Tab":
					
					return HttpResponseRedirect("add_drugs/tab")
					# return render(request, "drugs/add_drugs/tab", {"form":form})

				elif form.instance.state == "Suspension":
					return HttpResponseRedirect("add_drugs/suspension")

				else:
					return HttpResponseRedirect("add_drugs/injectable")
					
			else:
				drug = drug[0]

				#form.instance.id = drug.id
				#form.instance.stock_amount += drug.stock_amount

				update_stock(form, drug, price)
				
			# drug.cost_price = price
			add_stock(drug, price=cost_price)
			form = DrugForm()				
		else:
			# print("form")
			err_msg = f"Oops! Invalid form: {form.errors.as_text()}"
		
	else:
		form = DrugForm()
	return render(request, "drugs/add_drugs.html", {"form":form})


def sell_drugs(request, pk):
	# Determine if more than one drug is found with diff ststes before asking for state

	states = {"Tab":"Tablet", "Suspension":"Suspension", "Injectable":"Injectable"}
	price = 0.00
	# print(request.user.is_authenticated)

	if request.method == "GET":
		print(pk)
		form = SalesForm()
		drug = Drug.objects.filter(pk=pk)[0]
		drug_name = drug.drug_name
		brand_name = drug.brand_name
		weight = drug.weight
		form["drug_name"].initial = drug_name
		form["brand_name"].initial = brand_name
		form["weight"].initial = weight
		
		return render(request, "drugs/sell_drugs.html", {"form":form, "drug":drug})

	if request.method == "POST":
		# print(request.POST)
		form = SaleForm(request.POST)
		err_msg = ""

		#If the data is valid check if the drug exists
		# If so subtract from drug and register sales and credit
		if form.is_valid():
			form.upper()
			drug = Drug.objects.filter(drug_name=form.instance.drug_name, weight=form.instance.weight)
			if drug.count():
				drug = drug[0]
				price = drug.price
				form.instance.drug = drug
				if request.POST.get("add_sale_list"):
					form.add(drug)
					#print("list")
				elif request.POST.get("register_sale"):
					if request.POST.get("state") != drug.state:
						err_msg = f"Drug state \"{request.POST.get('state')}\" conflicts with \"{drug.state}\" "
					else:
						is_tab = False
						if request.POST.get("state") == "Tab":
							sell = form.instance.sell_tab
							if request.POST.get("tab-check"):
								is_tab = True
						elif request.POST.get("state") == "Suspension":
							sell = form.instance.sell_suspension
						else:
							sell = form.instance.sell_injectable

						try:
							# form.add(drug, is_tab, register=True)
							sell(is_tab=is_tab)
							credit(form.instance)
						except ValueError:
							if drug.out_of_stock == True:
								err_msg = f"{drug.drug_name} is not available at the moment!"
							else:
								err_msg = "The amount sold is more than available.\nPlease try again!"

						form = SaleForm()
				
			else:
				err_msg = "Drug not found!"
		return render(request, "drugs/sell_drugs.html", {"form":form, "err_msg":err_msg, "states":states, "price":price})
	else:
		form = SaleForm()
		return render(request, "drugs/sell_drugs.html", {"form":form, "states":states})


def add_stock(drug, price=0):
	"""add drug to stock and register debit"""
	_debit = Debit()
	_stock = Stock()

	_debit.item = str(drug)
	# _drug_no_tabs = int(drug.get_tab_cd()[0])
	_debit.amount = price
	_debit.save()

	_stock.drug = str(drug)
	_stock.price = price
	_stock.save()

def debit_stock(drug, price=0):
	"""subtract drug from stock and register credit"""
	_credit = Credit()
	_stock = Stock()

	_credit.item = str(drug)
	# _drug_no_tabs = int(drug.get_tab_cd()[0])
	_credit.amount = price
	_credit.save()

	_stock.drug = str(drug)
	_stock.price = price
	_stock.save()

def credit(sale):
	"""register credit"""
	_credit = Credit()
	_credit.item = str(sale)
	_credit.amount = sale.total_price
	_credit.save()

def restock(request, pk: int):
	# drug = Drug.objects.filter(pk=pk)
	drug = Drug.objects.get(pk=pk)
	form = DrugForm(instance=drug)

	# form.instance = drug
	# form.drug_name = "TEsst"
	if request.method == "POST":
		form = DrugForm(request.POST)
		if form.is_valid():
			add_drugs(request)

	return render(request, "drugs/add_drugs.html", {"form":form})


def edit(request, pk):
	drug = Drug.objects.get(pk=pk)
	form = DrugForm(instance=drug)

	if request.method == "POST":
		form = DrugForm(request.POST)
		if form.is_valid():
			pass

	return render(request, "drugs/add_drugs.html", {"form":form})



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
		context["headings"] = ["drug_name", "brand_name", "drug_type", "state", "weight",
							"manufacturer", "exp_date", "stock_amount", "price", "category",
							"purpose", "location"]
		return context
	
	def get(self, request, search=False):
		if not search:
			self.queryset = self.model.objects.all().order_by("drug_name")
		return super().get(request)


class SearchDrugs(ViewDrugs):
	#query = request["POST"]
	model = Drug
	

	def search(self, request):
		key = request.GET["search-box"].upper()
		queryset = Drug.objects.filter(drug_name__startswith=key)
		if not queryset:
			queryset = Drug.objects.filter(brand_name__startswith=key)

			# if not queryset:
			# 	# print("ALTERNATE")
			# 	drugs = [Drug.objects.all()[i].drug_name for i in range(len(Drug.objects.all()))]
			# 	drugs = [re.search(key, drug) for drug in drugs]

			# 	keys = []
			# 	for drug in drugs:
			# 		try:
			# 			keys.append(drug.string)
			# 		except AttributeError:
			# 			pass

			# 	queryset = keys
			# 	# print("RES")
			# 	print(keys)
		
		return queryset
	
	
	# queryset = search(request)
	def get(self, request):
		self.queryset = self.search(request).order_by("drug_name")
		return super().get(request, search=True)



	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


class ViewDrugDetails(ListView):
	model = Drug
	template_name = "drugs/details.html"
	context_object_name = "drug"
	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["d-class"] = "exp-far"
		context["headings"] = ["drug_name", "brand_name", "drug_type", "state", "weight",
							"manufacturer", "exp_date", "stock_amount", "price", "category",
							"purpose", "location"]
		return context
	
	def get(self, request, pk, search=False):
		if not search:
			self.queryset = self.model.objects.filter(pk=pk)[0]
		return super().get(request)


# class Restock(ListView):
# 	model = Drug
# 	template_name = "drugs/add_drugs.html"
# 	context_object_name = "drug"




class SellDrugs(ListView):
	model = Drug
	template_name = "drugs/sell_drug.html"
	list_template_name = "drugs/drugs.html"
	list_path = "../drugs"
	context_object_name = "drug"

	def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
		return super().get_context_data(**kwargs)
	
	def get(self, request, pk):
		drug = self.model.objects.filter(pk=pk)[0]

		form = SalesForm()
		drug_name = drug.drug_name
		brand_name = drug.brand_name
		weight = drug.weight
		state = drug.state

		if state != "Tab":
			form.fields["tab_state"].widget = form.fields["tab_state"].hidden_widget()

		form["drug_name"].initial = drug_name
		form["brand_name"].initial = brand_name
		form["weight"].initial = weight
		form["state"].initial = state
		form["price"].initial = 0
		form.fields["price"].widget = form.fields["price"].hidden_widget()

		return render(request, self.template_name, {"form": form, "drug":drug})
	
	def post(self, request, pk):
		drug = self.model.objects.filter(pk=pk)[0]
		
		form = SalesForm(request.POST)
		amount = int(form["amount"].value())
		stock = drug.stock_amount

		form.fields["price"].widget = form.fields["price"].hidden_widget()
		err_msg = ""
		# If the data is valid
		# Subtract from drug and register sales and credit
		if form.is_valid():
			form.upper()
			price = request.POST.get("price")
			form.instance.drug = drug

			if request.POST.get("add_sale_list"):
				form.add(drug)
				#print("list")
			elif request.POST.get("register_sale"):
				if request.POST.get("state") != drug.state:
					err_msg = f"Drug state \"{request.POST.get('state')}\" conflicts with \"{drug.state}\" "
				else:
					is_tab = True
					if request.POST.get("state") == "Tab":
						# print(request.POST)
						
						sell = form.instance.sell_tab
						if not request.POST.get("tab_state"):
							is_tab = False
							tb = int(drug.Tablet.get_tab_cd()[0])
							amount *= tb
						
					elif request.POST.get("state") == "Suspension":
						sell = form.instance.sell_suspension
					else:
						sell = form.instance.sell_injectable
					try:
						# form.add(drug, is_tab, register=True)
						# print(price)
						# print("==================================================================")
						# print(request.POST)
						
						if amount > stock:
							err_msg = f"Insufficient stock!!! \n{drug.clean_stock()} units left."
							return render(request, self.template_name, {"form":form, "drug":drug, "err_msg":err_msg})


						sell(is_tab=is_tab, price=price)
						credit(form.instance)
					except ValueError:
						if drug.out_of_stock == True:
							err_msg = f"{drug.drug_name} is not available at the moment!"
						else:
							err_msg = "The amount sold is more than available.\nPlease try again!"
					# form = SaleForm()
		return HttpResponse("<script type='text/javascript'>window.close();</script>")
		# return HttpResponseRedirect(self.list_path)
		# return render(request, self.template_name, {"form":form, "err_msg":err_msg})