from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormView
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


def add_drugs(request):
	if request.method =="POST":
		form = DrugForm(request.POST)
		
		# If the data is valid check if the drug with the same name, weight and exp_date exists
		# If not save the drug and register debit, else update existing drug
		if form.is_valid():
			drug = Drug.objects.filter(drug_name=form.instance.drug_name, weight=form.instance.weight, exp_date=form.instance.exp_date)
			if not drug.count():
				form.save()
				debit_stock(form.instance)
			else:
				drug = drug[0]
				form.instance.id = drug.id
				form.instance.stock_amount += drug.stock_amount
				form.save()
				debit_stock(drug)
			form = DrugForm()				
		else:
			err_msg = f"Oops! Invalid form: {form.errors.as_text()}"
		
	else:
		form = DrugForm()
	return render(request, "drugs/add_drugs.html", {"form":form})

def sell_drugs(request):
	if request.method == "POST":
		form = SaleForm(request.POST)

		#If the data is valid check if the drug exists
		# If so subtract from drug and register sales and credit
		if form.is_valid():
			drug = Drug.objects.filter(drug_name=form.instance.drug_name, weight=form.instance.weight)
			if drug.count():
				drug = drug[0]
				if request.POST.get("add_sale_list"):
					form.add(drug)
					print("list")
				elif request.POST.get("register_sale"):
					credit(form.instance)
					form.add(drug, register=True)
					form = SaleForm()
					
					print("reg!")
				#return HttpResponseRedirect("./sell_drugs", {"form": form})
				
			else:
				err_msg = "Drug not found!"
		return render(request, "drugs/sell_drugs.html", {"form":form})
	else:
		form = SaleForm()
		return render(request, "drugs/sell_drugs.html", {"form":form})


def debit_stock(drug):
	"""add drug to stock and register debit"""
	_debit = Debit()
	_stock = Stock()

	_debit.item = str(drug)
	_debit.amount = drug.price
	_debit.save()

	_stock.drug = drug
	_stock.price = drug.price
	_stock.save()

def credit(drug):
	"""register credit"""
	_credit = Credit()
	_credit.item = str(drug)
	_credit.amount = drug.total_price
	_credit.save()