from random import randint
from venv import create
from django.test import TestCase
from django.utils import timezone
from .models import Credit, Debit, Stock

# Create your tests here.

class CashChecks(TestCase):
	def check_credits(self, n=10):
		credits = []
		for i in range(n):
			amount = randint(5, 5000)
			credit = Credit.objects.create(item=f"credit-{i}", amount=amount)
		


	#create past and current credits

	#create past and current debits

	#check adding sales adds credits, and stock debits

	#create ane current bussiness month

	#test new and view bussiness values

	#test balances and checks