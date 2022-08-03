from django.db import models
from django.forms import IntegerField
from drugs.models import Drug

# Create your models here.

class BussinessMonth(models.Model):
	opening_cash = models.IntegerField()
	opening_stock = models.IntegerField()
	opening_date = models.DateField("date", auto_now_add=True)
	closing_cash = models.IntegerField(null=True)
	closing_stock = models.IntegerField(null=True)
	closing_date = models.DateField("date", null=True)
	profit = models.IntegerField(default=0)

	def calculate_profit(self):
		cash_profit = self.closing_cash - self.opening_cash
		stock_profit = self.closing_stock - self.opening_stock
		total_profit = cash_profit + stock_profit
		self.profit = total_profit
		self.save()

		return cash_profit, stock_profit, total_profit

class Credit(models.Model):
	item = models.CharField(max_length=200)
	amount = models.IntegerField()
	book_date = models.DateField("date", auto_now_add=True)

	def __str__(self) -> str:
		return f"Credit record of {self.item}"

class Debit(models.Model):
	item = models.CharField(max_length=200)
	amount = models.IntegerField()
	book_date = models.DateField("date", auto_now_add=True)

	def __str__(self) -> str:
		return f"Debit record of {self.item}"

class Stock(models.Model):
	drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
	price = IntegerField()
	balanced = models.BooleanField(default=True)

	def __str__(self):
		return f"Balancing of drug no {self.drug}"