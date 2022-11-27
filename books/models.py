from datetime import date
from django.db import models
from drugs.models import Sale

# Create your models here.

# A model to record cash and stock for each month
class BussinessMonth(models.Model):
	""" A bussiness month recording all transactions, profits and losses within the month """
	opening_cash = models.IntegerField()
	opening_stock = models.IntegerField()
	opening_date = models.DateField("opening date", auto_now_add=True)
	closing_cash = models.IntegerField(null=True)
	closing_stock = models.IntegerField(null=True)
	closing_date = models.DateField("closing date", null=True)
	profit = models.IntegerField(default=0)

	def any(self):
		""" Check if any bussiness month exists """
		bussiness_months = BussinessMonth.objects.get()
		if bussiness_months[0]:
			return True
		return False

	def balance_cash(self):
		""" Compute and return balances for cash transactions """
		credit = 0
		debit = 0

		# Filter transactions for the bussiness month and get the total credits and debits
		credits = Credit.objects.filter(book_date__month=self.opening_date.month)
		debits = Debit.objects.filter(book_date__month=self.opening_date.month)

		for item in credits:
			credit += item.amount
		
		for item in debits:
			debit += item.amount

		balance = self.opening_cash + credit - debit
		return balance

	def balance_stock(self):
		""" Compute and return balances for stock """
		sold_stock = 0
		added_stock = 0

		# Filter stock and sales by bussiness month and get total cost and sales
		sales = Sale.objects.filter(sale_time__month=self.opening_date.month)
		stock = Stock.objects.filter(date_added__month=self.opening_date.month)

		for sale in sales:
			sold_stock += sale.total_price
		
		for item in stock:
			added_stock += 5 #item.price

		balance = self.opening_stock + added_stock - sold_stock
		return balance

	def calculate_profit(self):
		""" Calculate the profit of a bussiness month """
		cash_profit = self.closing_cash - self.opening_cash
		stock_profit = self.closing_stock - self.opening_stock
		total_profit = cash_profit + stock_profit
		self.profit = total_profit
		self.save()
		#return cash_profit, stock_profit, total_profit

	def close(self):
		""" Close the accounts for the bussiness month """
		self.closing_cash = self.balance_cash()
		self.closing_stock = self.balance_stock()
		self.closing_date = date.today()
		self.calculate_profit()
		self.save()
	
	def __str__(self):
		return f"Bussiness month from {self.opening_date} to {self.closing_date}"


# A model to record all credit transactions
class Credit(models.Model):
	""" Records of all crediting transactions """
	item = models.CharField(max_length=200)
	amount = models.IntegerField()
	book_date = models.DateField("date", auto_now_add=True)

	def __str__(self) -> str:
		return f"Credit record of {self.item}"


# A model to record all debit transactions
class Debit(models.Model):
	""" Records of all debiting transactions """
	item = models.CharField(max_length=200)
	amount = models.IntegerField()
	book_date = models.DateField("date", auto_now_add=True)

	def __str__(self) -> str:
		return f"Debit record of {self.item}"


# A model to record all additions of stock
class Stock(models.Model):
	""" Records of all stock/drug transactions """
	# drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
	drug = models.CharField(max_length=100)
	price = models.IntegerField()
	date_added = models.DateField(auto_now_add=True)
	balanced = models.BooleanField(default=True)

	def __str__(self):
		return f"Balancing of drug no {self.drug}"