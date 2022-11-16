from random import randint
from venv import create
from django.test import TestCase
from django.utils import timezone
from .models import BussinessMonth, Credit, Debit, Stock

# Create your tests here.

class CashChecks(TestCase):
	def create_bussiness_month(self, n=4):
		for i in range(n):
			opening_cash = randint(50000, 100000)
			opening_stock = randint(50000, 100000)
			BussinessMonth.objects.create(opening_cash=opening_cash, opening_stock=opening_stock)

	def create_credits(self, n=10):
		for i in range(n):
			amount = randint(5, 5000)
			Credit.objects.create(item=f"credit-{i}", amount=amount)
	
	def create_debits(self, n=10):
		for i in range(n):
			amount = randint(5, 5000)
			Credit.objects.create(item=f"debit-{i}", amount=amount)
	
	def check_bussiness_month(self):
		self.create_bussiness_month(1)
		self.create_credits()
		self.create_debits()

		months = BussinessMonth.objects.all()
		for month in months:
			month.close()
			cash_profit = month.calculate_profits()[0]
			

		
	


	#create past and current credits

	#create past and current debits

	#check adding sales adds credits, and stock debits

	#create ane current bussiness month

	#test new and view bussiness values

	#test balances and checks