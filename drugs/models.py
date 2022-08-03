from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Drug(models.Model):
	drug_name = models.CharField(max_length=30)
	brand_name = models.CharField(max_length=30)
	drug_type = models.CharField(max_length=10)
	weight = models.CharField(max_length=10)
	manufacturer = models.CharField(max_length=30)
	exp_date = models.DateField("Expiery Date")
	stock_amount = models.IntegerField()
	price = models.IntegerField()
	category = models.CharField(max_length=30)
	purpose = models.CharField(max_length=30)
	location = models.CharField(max_length=10)
	day_added = models.DateField(null=True, auto_now_add=True)
	out_of_stock = models.BooleanField(default=False)
	expired = models.BooleanField(default=False)

	def check_exp(self):
		pass

	def sell(self, amount: int):
		self.stock_amount -= amount
		if self.stock_amount == 0:
			self.out_of_stock = True
		elif self.stock_amount < 0:
			raise ValueError(f"amount {amount} greater than stock amount")

	def relocate(self, new_location: str):
		self.location = new_location

	def __str__(self):
		return f" {self.drug_name}: A drug for {self.purpose} located at {self.location}.\
			 Expires: {self.exp_date} "

class Sale(models.Model):
	#drug = models.ForeignKey(Drug, on_delete=CASCADE)
	drug_name = models.CharField(max_length=30)
	brand_name = models.CharField(max_length=30)
	weight = models.CharField(max_length=10)
	amount = models.IntegerField()
	total_price = models.IntegerField(default=0)
	sale_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Sale of {self.drug_name}"