from django import forms
from .models import Drug, Sale

class DrugForm(forms.ModelForm):
	class Meta:
		model = Drug
		fields = ["drug_name", "brand_name", "drug_type", "weight",
		"manufacturer", "exp_date", "stock_amount", "price", "category",
		"purpose", "location"]

class SaleForm(forms.ModelForm):
	class Meta:
		model = Sale
		fields = ["drug_name", "brand_name", "weight", "amount"]
	
	names = []
	ids = []
	total_price = 0
	

	def add(self, drug, register=False):
		
		# print(self.i)
		# if not self.i:
		# 	self.names = []
		# 	self.i += 1
		sale = super(SaleForm, self).save(commit=False)
		print(sale)
		print(sale.drug_name)
		print(self.instance.total_price)
		
		
		self.add_list(sale, drug)

		print(sale.drug_name)
		print(sale.drug_name)
		print(self.instance.drug_name)

		drug.sell(sale.amount)
		drug.save()
		if register:
			sale.save()
			print(self.fields)
			return self.total_price

	def add_list(self, sale, drug):
		self.names.append(sale.drug_name)
		self.ids.append(drug.id)
		self.total_price += (drug.price * sale.amount)
		sale.drug_name = ", ".join(self.names)
		sale.total_price = self.total_price