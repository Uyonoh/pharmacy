from django import forms
from django.db import models
from .models import Drug, Sale, Tablet

unit_choices = (("Cartons", "Cartons"), ("Packets", "Packets"), ("Sachets", "Sachets"))

# class SubDrug(Drug):
# 	units = models.CharField(max_length=30, choices=unit_choices, default="Packets")
# 	# ch = models.BooleanField("bin1", max_length=2, default=False)
# 	# ch = models.BinaryField("bina", max_length=10, choices=unit_choices)

class DrugForm(forms.ModelForm):
	class Meta:
		model = Tablet
		fields = ["drug_name", "brand_name", "drug_type", "state", "tab_cd", "weight",
		"manufacturer", "exp_date", "units", "purchase_amount", "price", "category",
		"purpose", "location"]

	def save(self, first_stock=True):
		form = super(DrugForm, self).save(commit=False)
		for field in ["drug_name", "brand_name", "drug_type", "manufacturer", "category", "purpose", "location"]:
			val = getattr(form, field)
			if val:
				setattr(form, field, val.upper())
		form.save(first_stock)

class SaleForm(forms.ModelForm):
	class Meta:
		model = Sale
		fields = ["drug_name", "brand_name", "weight", "amount"]
	
	names = []
	ids = []
	total_price = 0
	

	def add(self, drug, is_tab, register=False):
		
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
		