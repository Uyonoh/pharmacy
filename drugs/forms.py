from .models import Drug, Sale, Tablet, Suspension, Injectable, state_choices
from .customs import *
from django import forms
from django.utils import timezone as tz

unit_choices = (("Cartons", "Cartons"), ("Packets", "Packets"), ("Sachets", "Sachets"))
units_list = ["cart", "pack", "sach"]

# datalist and moeldatalist widgets


	

class DrugForm(forms.ModelForm):
	# drug_name = ModelChoiceField(model=Drug, field="drug_name", check=False)
	# brand_name = ModelChoiceField(model=Drug, field="brand_name", check=False)
	# drug_type = ModelChoiceField(model=Drug, field="drug_type", check=False)
	sale_price = forms.DecimalField(decimal_places=2)
	class Meta:
		model = Drug
		fields = ["drug_name", "brand_name", "drug_type", "state", "weight",
		"manufacturer", "exp_date", "units", "purchase_amount", "cost_price", "sale_price", "category",
		"purpose", "location"]

	def upper(self):
		# try:
		# 	v = getattr(self, "drug_name")()
		# except ValidationError as e:
		# 	print(f"error 2 - {e.message}")
			
		form = super(DrugForm, self).save(commit=False)
		for field in ["drug_name", "brand_name", "drug_type", "manufacturer", "category", "purpose", "location"]:
			val = getattr(form, field)
			if val:
				setattr(form, field, val.upper())

	def save(self, commit=False):
		form = super(DrugForm, self).save(commit=False)
		form.save(commit)

class TabletForm(forms.ModelForm):
	class Meta:
		model = Tablet
		fields = ["tab_cd", "no_packs"]

		def save(self):
			super(TabletForm, self).save()

class SuspensionForm(forms.ModelForm):
	class Meta:
		model = Suspension
		fields = ["no_bottles", "no_packs"]

class InjectableForm(forms.ModelForm):
	class Meta:
		model = Injectable
		fields = ["no_bottles", "no_packs"]

class SaleForm(forms.ModelForm):
	# state = ChoiceField(choices=units_list, list=True)
	state = forms.ChoiceField( choices=state_choices)
	# status = ChoiceField(widget=DataList, choices=units_list, list=True)
	drug_name = ModelChoiceField(model=Drug, field="drug_name")
	brand_name = ModelChoiceField(model=Drug, field="brand_name")
	class Meta:
		model = Sale
		fields = ["drug_name", "brand_name", "weight", "amount"]
	
	names = []
	ids = []
	total_price = 0
	
	def upper(self):
		form = super(SaleForm, self).save(commit=False)
		for field in ["drug_name", "brand_name"]:
			val = getattr(form, field)
			if val:
				setattr(form, field, val.upper())

	def add(self, drug, is_tab = False, register=False):
		
		# print(self.i)
		# if not self.i:
		# 	self.names = []
		# 	self.i += 1
		sale = super(SaleForm, self).save(commit=False)
		print(sale)
		print(sale.drug_name)
		print(self.instance.total_price)
		
		
		#self.add_list(sale, drug)

		print(sale.drug_name)
		print(sale.drug_name)
		print(self.instance.drug_name)


		drug.sell(sale.amount, is_tab)
		if register:
			sale.save()
			print(self.fields)
			return self.total_price

	def add_list(self, sale, drug):
		#self.names = sale.drug_name.append(sale.drug_name)
		self.ids.append(drug.id)
		self.total_price += (drug.price * sale.amount)
		sale.drug_name = sale.drug_name #", ".join(self.names)
		sale.total_price = self.total_price
		
class SalesForm(forms.ModelForm):
	# state = ChoiceField(choices=units_list, list=True)
	state = forms.CharField(max_length=30, label="State")
	price = forms.FloatField(label="Price")
	tab_state = forms.BooleanField(required=False, label="Tab")
	time_toggle = forms.BooleanField(required=False, label="Change Time")
	sale_time = forms.DateTimeField(initial=tz.now())
	# price = forms.HiddenInput()

	# # status = ChoiceField(widget=DataList, choices=units_list, list=True)
	# drug_name = forms.TextInput()
	# brand_name = forms.TextInput()

	class Meta:
		model = Sale
		fields = ["drug_name", "brand_name", "weight", "amount"]
		# labels = {"drug_name": "drug_name", "brand_name": "brand_name", "weight": "weight", "amount": "amount"}
	
	names = []
	ids = []
	total_price = 0
	
	def upper(self):
		form = super(SalesForm, self).save(commit=False)
		for field in ["drug_name", "brand_name"]:
			val = getattr(form, field)
			if val:
				setattr(form, field, val.upper())

	def add(self, drug, is_tab = False, register=False):
		
		# print(self.i)
		# if not self.i:
		# 	self.names = []
		# 	self.i += 1
		sale = super(SalesForm, self).save(commit=False)
		print(sale)
		print(sale.drug_name)
		print(self.instance.total_price)
		
		
		#self.add_list(sale, drug)

		print(sale.drug_name)
		print(sale.drug_name)
		print(self.instance.drug_name)


		drug.sell(sale.amount, is_tab)
		if register:
			sale.save()
			print(self.fields)
			return self.total_price

	def add_list(self, sale, drug):
		#self.names = sale.drug_name.append(sale.drug_name)
		self.ids.append(drug.id)
		self.total_price += (drug.price * sale.amount)
		sale.drug_name = sale.drug_name #", ".join(self.names)
		sale.total_price = self.total_price