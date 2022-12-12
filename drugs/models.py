from datetime import date
from xmlrpc.client import Boolean
from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# option to select purchase units
# 

state_choices = (("Tab", "Tab"), ("Suspension", "Suspension"), ("Injectable", "Injectable"))
unit_choices = (("Cartons", "Cartons"), ("Packets", "Packets"), ("Unit", "Sachets/Bottle/Card"))

class Drug(models.Model):
	""" Base drug class """
	drug_name = models.CharField(max_length=30)
	brand_name = models.CharField(max_length=30)
	drug_type = models.CharField(max_length=10)
	state = models.CharField(max_length=20, choices=state_choices, default="Tab")
	weight = models.CharField(max_length=10)
	manufacturer = models.CharField(max_length=30)
	exp_date = models.DateField("Expiery Date")
	stock_amount = models.IntegerField()
	purchase_amount = models.IntegerField()
	units = models.CharField(max_length=30, choices=unit_choices, default="Packets")
	# price = models.IntegerField()
	# carton_price = models.IntegerField(null=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
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
		self.stock_amount = self.purchase_amount * int(no_tabs)

		if self.units == "Unit":
			self.stock_amount *= int(no_cards) 

		if self.units == "Cartons":
			self.stock_amount = self.stock_amount * self.no_packs

	# def set_price(self):
	# 	# self.price = self.price / int(self.get_tab_cd()[1])
	# 	print(self.price)
	# 	if self.units == "Cartons":
	# 		price = self.price / self.purchase_amount			#price per carton
	# 		price = price / self.no_packs			#price per pack
	# 		price = price / int(self.get_tab_cd()[1])			#price per card
	# 		self.price = price
	# 	else:
	# 		price  = self.price / self.purchase_amount			#price per pack
	# 		print(price)
	# 		print(f"amount - {self.purchase_amount}")
	# 		price = price / int(self.get_tab_cd()[1])	
	# 		print(price)		#price per card
	# 		print(f'cd - {self.get_tab_cd()[1]}')
	# 		self.price = price
		
	# 	return True

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
	no_packs = models.IntegerField(null=True, default=0)
	# carton_price = models.IntegerField(null=True)

	def get_tab_cd(self):
		return self.tab_cd.split("/")

	def set_amount(self):
		no_tabs, no_cards = self.get_tab_cd()
		amount = self.drug.purchase_amount * int(no_tabs)

		if self.drug.units == "Packets":
			amount *= int(no_cards) 

		if self.drug.units == "Cartons":
			amount = amount * self.no_packs * int(no_cards) 

		return amount

	def set_price(self):
		price  = self.drug.price / self.drug.purchase_amount # price per carton or pack
		if self.drug.units == "Packets":
			price = price / int(self.get_tab_cd()[1])	
			
		elif self.drug.units == "Cartons":
			price = price / self.no_packs			#price per pack
			price = price / int(self.get_tab_cd()[1])			#price per card
			
		self.drug.price = price
		return price

	def sell(self, amount: int, units="Units", is_tab: Boolean=False):
		if is_tab:
			self.drug.stock_amount -= amount
		else:
			no_tabs, no_cards = self.get_tab_cd()
			amount = amount * int(no_tabs)

			if units == "Packets":
				amount *= int(no_cards)
			elif units == "Cartons":
				amount *= int(no_cards)
				amount *= self.no_packs

			self.drug.stock_amount -= amount
			if self.drug.stock_amount == 0:
				self.drug.out_of_stock = True
			elif self.drug.stock_amount < 0:
				raise ValueError(f"amount {amount} greater than stock amount")
		self.drug.save()

	def save(self, first_stock=True, sale=False):
		if not sale:
			self.set_price()
		if first_stock:
			self.drug.stock_amount = self.set_amount()
		self.drug.save()
		return super(Tablet, self).save()

	def tabulate(self):
		return (self.drug_name, self.brand_name, self.drug_type, self.weight,
			self.manufacturer, self.exp_date, self.stock_tab_cd(), self.price, self.category, self.purpose,
			self.location, self.day_added, self.out_of_stock, self.expired)

	def update_stock(self, new_amount, units, price):
		self.drug.purchase_amount = new_amount
		self.drug.units = units
		old_price = self.drug.price
		self.drug.price = price
		if not price == old_price:
			self.drug.old_price = old_price
		self.drug.save()
		new_amount = self.set_amount()
		self.drug.stock_amount += new_amount
		self.set_price()
		self.drug.save()
		
	def __str__(self):
		return f" {self.drug.drug_name} Tablet: A drug for {self.drug.purpose} located at {self.drug.location}.\
			 Expires: {self.drug.exp_date} "

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
	drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
	no_bottles = models.IntegerField(null=True)
	no_packs = models.IntegerField(null=True, default=0)

	def set_amount(self):
		amount = self.drug.purchase_amount
		if self.drug.units == "Packets":
			amount *= self.no_bottles
		elif self.drug.units == "Cartons":
			amount *= self.no_packs
			amount *= self.no_bottles
		return amount

	def set_price(self):
		price = self.drug.price / self.drug.purchase_amount	
		if self.drug.units == "Cartons":
			price = price / self.no_packs			#price per pack
			price = price / self.no_bottles			#price per bottle	
		elif self.drug.units == "Packets":			
			price = price / self.no_bottles		#price per card
		self.drug.price = price
		return price
	
	def sell(self, amount: int, units="Units"):
		
		if units == "Packets":
			amount *= self.no_bottles
		elif units == "Cartons":
			amount *= self.no_bottles
			amount *= self.no_packs
   
		self.drug.stock_amount -= amount
		if self.drug.stock_amount == 0:
			self.drug.out_of_stock = True
		elif self.drug.stock_amount < 0:
			raise ValueError(f"amount {amount} greater than stock amount")
		self.drug.save()

	def save(self, first_stock=True, sale=False):
		if not sale:
			self.set_price()
		if first_stock:
			self.drug.stock_amount = self.set_amount()
		self.drug.save()
		return super(Suspension, self).save()

	def tabulate(self):
		return (self.drug_name, self.brand_name, self.drug_type, self.weight,
			self.manufacturer, self.exp_date, self.stock_tab_cd(), self.price, self.category, self.purpose,
			self.location, self.day_added, self.out_of_stock, self.expired)

	def update_stock(self, new_amount, units, price):
		self.drug.purchase_amount = new_amount
		self.drug.units = units
		old_price = self.drug.price
		self.drug.price = price
		if not price == old_price:
			self.drug.old_price = old_price
		# self.drug.save()
		new_amount = self.set_amount()
		self.drug.stock_amount += new_amount
		self.set_price()
		self.drug.save()

	def __str__(self):
		return f" {self.drug.drug_name} Suspension: A drug for {self.drug.purpose} located at {self.drug.location}.\
			 Expires: {self.drug.exp_date} "
		

class Injectable(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
	no_bottles = models.IntegerField(null=True)
	no_packs = models.IntegerField(null=True, default=0)

	def set_amount(self):
		amount = self.drug.purchase_amount
		if self.drug.units == "Packets":
			amount *= self.no_bottles
		elif self.drug.units == "Cartons":
			amount *= self.no_packs
			amount *= self.no_bottles
		return amount

	def set_price(self):
		price = self.drug.price / self.drug.purchase_amount	
		if self.drug.units == "Cartons":
			price = price / self.no_packs			#price per pack
			price = price / self.no_bottles			#price per bottle	
		elif self.drug.units == "Packets":			
			price = price / self.no_bottles		#price per card
		self.drug.price = price
		return price
	
	def sell(self, amount: int, units="Units"):
		
		if units == "Packets":
			amount *= self.no_bottles
		elif units == "Cartons":
			amount *= self.no_bottles
			amount *= self.no_packs
   
		self.drug.stock_amount -= amount
		if self.drug.stock_amount == 0:
			self.drug.out_of_stock = True
		elif self.drug.stock_amount < 0:
			raise ValueError(f"amount {amount} greater than stock amount")
		self.drug.save()

	def save(self, first_stock=True, sale=False):
		if not sale:
			self.set_price()
		if first_stock:
			self.drug.stock_amount = self.set_amount()
		self.drug.save()
		return super(Injectable, self).save()

	def tabulate(self):
		return (self.drug_name, self.brand_name, self.drug_type, self.weight,
			self.manufacturer, self.exp_date, self.stock_tab_cd(), self.price, self.category, self.purpose,
			self.location, self.day_added, self.out_of_stock, self.expired)

	def update_stock(self, new_amount, units, price):
		self.drug.purchase_amount = new_amount
		self.drug.units = units
		old_price = self.drug.price
		self.drug.price = price
		if not price == old_price:
			self.drug.old_price = old_price
		# self.drug.save()
		new_amount = self.set_amount()
		self.drug.stock_amount += new_amount
		self.set_price()
		self.drug.save()


	def __str__(self):
		return f" {self.drug.drug_name} Injectable: A drug for {self.drug.purpose} located at {self.drug.location}.\
			 Expires: {self.drug.exp_date} "		

class Sale(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
	drug_name = models.CharField(max_length=30)
	brand_name = models.CharField(max_length=30)
	weight = models.CharField(max_length=10)
	amount = models.IntegerField(default=1)
	total_price = models.IntegerField(null=True)
	sale_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Sale of {self.drug_name}"
	
	def sell_tab(self, **kwargs):
		is_tab = kwargs["is_tab"]
		self.total_price = self.drug.price * self.amount
		if is_tab:
			self.total_price = self.total_price / int(self.drug.Tablet.get_tab_cd()[0])
			self.drug_name += " - TAB"
		
		self.drug.tablet_set.all()[0].sell(self.amount, is_tab)
		self.save()
		

	def sell_suspension(self, **kwargs):
		
		self.total_price = self.drug.price * self.amount
		self.drug.suspension_set.all()[0].sell(self.amount)
		self.save()

	def sell_injectable(self, **kwargs):
		self.total_price = self.drug.price * self.amount
		self.drug.injectable_set.all()[0].sell(self.amount)
		self.save()