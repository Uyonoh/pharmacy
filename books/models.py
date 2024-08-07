from datetime import date
from django.db import models
from drugs.models import Sale
from django.utils import timezone as tz

# Create your models here.

# A model to record cash and stock for each month
class BussinessMonth(models.Model):
	""" A bussiness month recording all transactions, profits and losses within the month """
	opening_cash = models.IntegerField()
	opening_stock = models.IntegerField()
	opening_date = models.DateField("opening date", default=tz.now().date())
	closing_cash = models.IntegerField(null=True)
	closing_stock = models.IntegerField(null=True)
	closing_date = models.DateField("closing date", null=True)
	profit = models.IntegerField(default=0)

	def any(self) -> bool:
		""" Check if any bussiness month exists """
		bussiness_months = BussinessMonth.objects.get()
		if bussiness_months[0]:
			return True
		return False
	
	def get_credits(self, closing=None) -> int:
		credit = 0

		if not closing:
			closing = self.closing

		# credits = Credit.objects.filter(book_date__month=self.opening_date.month)
		credits = Credit.objects.filter(book_date__gte=self.opening_date)
		credits = credits.filter(book_date__lte=closing)
		for item in credits:
			credit += item.amount
		return credit

	def get_debits(self, closing=None) -> int:
		debit = 0

		if not closing:
			closing = self.closing

		debits = Debit.objects.filter(book_date__gte=self.opening_date)
		debits = debits.filter(book_date__lte=closing)
		for item in debits:
			debit += item.amount
		return debit
	
	def get_sales(self, closing=None) -> int:
		sold_stock = 0

		if not closing:
			closing = self.closing

		sales = Sale.objects.filter(sale_time__date__gte=self.opening_date)
		sales = sales.filter(sale_time__date__lte=closing)

		for sale in sales:
			sold_stock += sale.total_price

		return sold_stock
	
	def get_sale_costs(self, closing=None):
		""" Returns the price of drugs sold at cost prices """
		sold_stock = 0

		if not closing:
			closing = self.closing

		sales = Sale.objects.filter(sale_time__date__gte=self.opening_date)
		sales = sales.filter(sale_time__date__lte=closing)

		for sale in sales:
			sold_stock += sale.cost_price

		return sold_stock

	def get_stocks(self, closing=None) -> int:
		added_stock = 0

		if not closing:
			closing = self.closing

		stocks = Stock.objects.filter(date_added__gte=self.opening_date)
		stocks = stocks.filter(date_added__lte=closing)

		for item in stocks:
			added_stock += item.price

		return added_stock


	def balance_cash(self) -> int:
		""" Compute and return balances for cash transactions """
		
		# Filter transactions for the bussiness month and get the total credits and debits
		credit = self.get_credits()
		debit = self.get_debits()
		
		balance = self.opening_cash + credit - debit
		return balance

	def balance_stock(self) -> int:
		""" Compute and return balances for stock """
		# sold_stock = 0
		# added_stock = 0

		# # Filter stock and sales by bussiness month and get total cost and sales
		# sales = Sale.objects.filter(sale_time__month=self.opening_date.month)
		# stock = Stock.objects.filter(date_added__month=self.opening_date.month)

		# for sale in sales:
		# 	sold_stock += sale.total_price
		
		# for item in stock:
		# 	added_stock += item.price
		sold_stock = self.get_sales()
		added_stock = self.get_stocks()

		balance = self.opening_stock + added_stock - sold_stock
		return balance

	def calculate_profit(self, commit=True) -> None:
		""" Calculate the profit of a bussiness month """
		cash_income = self.get_credits() - self.get_debits()
		stock_outflow = self.get_stocks() - self.get_sales()
		sale_profit = self.get_sales() - self.get_sale_costs()
		# total_profit = cash_income + stock_outflow
		self.profit = sale_profit
		if commit:
			self.save()
		#return cash_profit, stock_profit, total_profit

	def close(self, dates=[]) -> None:
		""" Close the accounts for the bussiness month """
		self.closing_cash = self.balance_cash()
		self.closing_stock = self.balance_stock()
		self.closing_date = date.today()
		if dates and len(dates) == 3:
			try:
				self.closing_date = date(dates[0], dates[1], dates[2])
			except Exception:
				raise ValueError(f"Invalid date list: {dates}. Must be[y, m, d]")
		self.calculate_profit()
		self.save()
	
	@property
	def closing(self):
		if self.closing_date:
			return self.closing_date
		else:
			return tz.now().date()

	def __str__(self) -> str:
		return f"Bussiness month from {self.opening_date} to {self.closing_date}"


# A model to record all credit transactions
class Credit(models.Model):
	""" Records of all crediting transactions """
	item = models.CharField(max_length=200)
	amount = models.IntegerField()
	book_date = models.DateField("date", default=str(tz.now().date()))

	def __str__(self) -> str:
		return f"Credit record of {self.item}"


# A model to record all debit transactions
class Debit(models.Model):
	""" Records of all debiting transactions """
	item = models.CharField(max_length=200)
	amount = models.IntegerField()
	book_date = models.DateField("date", default=str(tz.now().date()))

	def __str__(self) -> str:
		return f"Debit record of {self.item}"


# A model to record all additions of stock
class Stock(models.Model):
	""" Records of all stock/drug transactions 'prices' """
	# drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
	drug = models.CharField(max_length=100)
	price = models.IntegerField()
	date_added = models.DateField("date", default=str(tz.now().date()))
	balanced = models.BooleanField(default=True)
	

	def __str__(self) -> str:
		return f"Balancing of drug no {self.drug}"
