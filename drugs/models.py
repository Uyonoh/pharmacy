from datetime import date
from xmlrpc.client import Boolean
from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# option to select purchase units
# 

state_choices = (("Tab", "Tab"), ("Suspension", "Suspension"), ("Injectable", "Injectable"))
unit_choices = (("Cartons", "Cartons"), ("Packets", "Packets"), ("Sachets", "Sachets"))

class Drug(models.Model):
	""" Base drug class """
	drug_name = models.CharField(max_length=30)
	brand_name = models.CharField(max_length=30)
	drug_type = models.CharField(max_length=10)
	state = models.CharField(max_length=20, choices=state_choices)
	weight = models.CharField(max_length=10)
	manufacturer = models.CharField(max_length=30)
	exp_date = models.DateField("Expiery Date")
	stock_amount = models.IntegerField()
	purchase_amount = models.IntegerField()
	units = models.CharField(max_length=30, choices=unit_choices, default="Packets")
	# price = models.IntegerField()
	# carton_price = models.IntegerField(null=True)
	price = models.IntegerField()
	category = models.CharField(max_length=30)
	purpose = models.CharField(max_length=30)
	location = models.CharField(max_length=10)
	day_added = models.DateField(null=False, auto_now_add=True)
	out_of_stock = models.BooleanField(default=False)
	expired = models.BooleanField(default=False, null=True)


	def check_exp(self):
		diff = self.exp_date - date.today()
		days = diff.days
		return days

	def expired(self):
		return self.check_exp() <= 0
	
	def expire_soon(self):
		return self.check_exp() <= 90

	def relocate(self, new_location: str):
		self.location = new_location

	def set_amount(self):
		no_tabs, no_cards = self.get_tab_cd()
		self.stock_amount = self.purchase_amount * int(no_cards) * int(no_tabs)

		if self.units == "Cartons":
			self.stock_amount = self.stock_amount * self.no_packs

	def set_price(self):
		# self.price = self.price / int(self.get_tab_cd()[1])
		print(self.price)
		if self.units == "Cartons":
			price = self.price / self.purchase_amount			#price per carton
			price = price / self.no_packs			#price per pack
			price = price / int(self.get_tab_cd()[1])			#price per card
			self.price = price
		else:
			price  = self.price / self.purchase_amount			#price per pack
			print(price)
			print(f"amount - {self.purchase_amount}")
			price = price / int(self.get_tab_cd()[1])	
			print(price)		#price per card
			print(f'cd - {self.get_tab_cd()[1]}')
			self.price = price
		
		return True

	def sell(self, amount: int, is_tab: Boolean):
		self.stock_amount -= amount
		if self.stock_amount == 0 and self.remainder == 0:
			self.out_of_stock = True
		elif self.stock_amount < 0:
			raise ValueError(f"amount {amount} greater than stock amount")
		self.save(first_stock=False, sale=True)

	# def save(self, sale=False):
	# 	if not sale:
	# 		self.set_price()
	# 	return super(Drug, self).save()

	def tabulate(self):
		return (self.drug_name, self.brand_name, self.drug_type, self.weight,
			self.manufacturer, self.exp_date, self.stock_amount, self.price, self.category, self.purpose,
			self.location, self.day_added, self.out_of_stock, self.expired)

	def update_stock(self, new_amount):
		pass

	def __str__(self):
		return f" {self.drug_name}: A drug for {self.purpose} located at {self.location}.\
			 Expires: {self.exp_date} "

class Tablet(models.Model):
	# tab_id = models.AutoField(primary_key=True)
	drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
	tab_cd = models.CharField(max_length=10, null=True)
	remainder = models.IntegerField(null=True, default=0)
	no_packs = models.IntegerField(null=True, default=0)
	# carton_price = models.IntegerField(null=True)

	def get_tab_cd(self):
		return self.tab_cd.split("/")

	def set_amount(self):
		no_tabs, no_cards = self.get_tab_cd()
		self.drug.stock_amount = self.drug.purchase_amount * int(no_cards) * int(no_tabs)

		if self.drug.units == "Cartons":
			self.stock_amount = self.stock_amount * self.no_packs

	def set_price(self):
		# self.price = self.price / int(self.get_tab_cd()[1])
		# print(self.price)
		price  = self.drug.price / self.drug.purchase_amount # price per carton or pack
		if self.drug.units == "Cartons":
			price = price / self.no_packs			#price per pack
			price = price / int(self.get_tab_cd()[1])			#price per card
			self.drug.price = price
		else:
			# print(price)
			# print(f"amount - {self.drug.purchase_amount}")
			price = price / int(self.get_tab_cd()[1])	
			print(price)		#price per card
			print(f'cd - {self.get_tab_cd()[1]}')
			self.drug.price = price
		
		return True

	def sell(self, amount: int, is_tab: Boolean):
		if is_tab:
			self.drug.stock_amount -= amount
		else:
			no_tabs, no_cards = self.get_tab_cd()
			amount = amount * int(no_tabs)
			self.drug.stock_amount -= amount
			if self.drug.stock_amount == 0 and self.remainder == 0:
				self.drug.out_of_stock = True
			elif self.drug.stock_amount < 0:
				raise ValueError(f"amount {amount} greater than stock amount")
		self.drug.save()

	def save(self, first_stock=True, sale=False):
		if not sale:
			self.set_price()
		if first_stock:
			self.set_amount()
		self.drug.save()
		return super(Tablet, self).save()

	def stock_tab_cd(self):
		no_tab, no_cd = self.get_tab_cd()
		no_tab, no_cd = int(no_tab), int(no_cd)

		stock_cd = self.stock_amount // no_tab
		stock_tab = self.stock_amount % no_tab

		return f"{stock_cd}.{stock_tab}"

	def tabulate(self):
		return (self.drug_name, self.brand_name, self.drug_type, self.weight,
			self.manufacturer, self.exp_date, self.stock_tab_cd(), self.price, self.category, self.purpose,
			self.location, self.day_added, self.out_of_stock, self.expired)

	def update_stock(self, new_amount):
		pass

	# def __str__(self):
	# 	return f" {self.drug_name}: A drug for {self.purpose} located at {self.location}.\
	# 		 Expires: {self.exp_date} "


	@property
	def tab_price(self):
		no_tab = self.get_tab_cd()[0]
		no_tab = int(no_tab)

		card_price = self.price
		price = card_price / no_tab

		return price
	
	@property
	def card_price(self):
		return self.price

	@property
	def pack_price(self):
		price = price * int(self.get_tab_cd()[1])

		return price

	@property
	def carton_price(self):
		price = self.price
		price = price * int(self.get_tab_cd()[1]) * self.no_packs

		return price

class Suspension(models.Model):
	pass

class Injectable(models.Model):
	pass

class Sale(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
	drug_name = models.CharField(max_length=30)
	brand_name = models.CharField(max_length=30)
	weight = models.CharField(max_length=10)
	amount = models.IntegerField()
	total_price = models.IntegerField(null=True)
	sale_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Sale of {self.drug_name}"
	
	def compute_tab(self, is_tab):
		self.total_price = self.drug.price * self.amount
		if is_tab:
			self.total_price = self.total_price / int(self.drug.Tablet.get_tab_cd()[0])
			self.drug_name += " - TAB"
		try:
			self.drug.tablet_set.all()[0].sell(self.amount, is_tab)
			self.save()
		except:
			return 0


	def compute_suspension(self):
		self.total_price = self.drug.price * self.amount

	def compute_injectable(self):
		self.total_price = self.drug.price * self.amount
