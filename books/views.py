from datetime import date
from django.http import HttpResponseRedirect
from django.shortcuts import render
from drugs.models import Sale
from books.models import BussinessMonth, Credit, Debit, Stock
from .forms import BussinessMonthForm

# Create your views here.

def new_bussiness_month(request):
	""" View to create new bussiness month """

	# Get all bussiness months
	months = BussinessMonth.objects.all()

	#if no bussiness months, create new month else go to view bussiness months
	if not months:
		form = BussinessMonthForm(request.POST)
		if form.is_valid():
			form.save()
		return render(request, "books/newbussinessmonth.html", {"form":form})
	else:
		return HttpResponseRedirect("viewbussinessmonth") #(request, "books/viewbussinessmonth.html", {"dr":2})

def view_bussiness_month(request):
	""" View for bussiness month """

	# Try to create new bussiness month
	months = BussinessMonth.objects.all()

	if months:
		# If bussiness month exists filter current month and calculate
		# this month's opening amounts from last month's closing amounts

		# If this is the first bussiness month display error msg
		# as there is no previous month to use for computations
		if months.count() == 1 and months[0].opening_date.month == date.today().month:
			err_msg = "There is no record as this is the first bussiness month! Please try again next month."
			return render(request, "books/viewbussinessmonth.html", {"err_msg": err_msg})

		# The number for the last month
		month_ = date.today().month-1
		if month_ == 0:
			month_ = 12
		last_month = months.filter(opening_date__month=month_)[0]

		# If the current month's opening amounts do not exist then
		# calculate them
		if not months.filter(opening_date__month=date.today().month):
			last_month.close()
			
			this_month = BussinessMonth()
			this_month.opening_cash = last_month.closing_cash
			this_month.opening_stock = last_month.closing_stock
			this_month.save()
		else:
			this_month = months.filter(opening_date__month=date.today().month)[0]

		month_view = {
			"last_opening_cash": last_month.opening_cash,
			"last_opening_stock": last_month.opening_stock,
			"last_closing_cash": last_month.closing_cash,
			"last_closing_stock": last_month.closing_stock,
			"last_profit": last_month.profit,
			"credits": last_month.get_credits(),
			"debits": last_month.get_debits()
			}
		
		return render(request, "books/viewbussinessmonth.html", {"view": month_view})
	
	# create new bussiness month if none exists
	initialize(0, 0)
	# view_bussiness_month(request)
	return view_bussiness_month(request)	


# def balance_cash(last_opening_cash):
# 	""" Compute and return balances for cash transactions """
# 	credit = 0
# 	debit = 0

# 	# Filter transactions for the past month and get the total credits and debits
# 	credits = Credit.objects.filter(book_date__month=date.today().month-1)
# 	debits = Debit.objects.filter(book_date__month=date.today().month-1)

# 	for item in credits:
# 		credit += item.amount
	
# 	for item in debits:
# 		debit += item.amount

# 	balance = last_opening_cash + credit - debit
# 	return balance

# def balance_stock(last_opening_stock):
# 	""" Compute and return balances for stock """
# 	sold_stock = 0
# 	added_stock = 0

# 	# Filter stock and sales by past month and get total cost and sales
# 	sales = Sale.objects.filter(sale_time__month=date.today().month-1)
# 	stock = Stock.objects.all()

# 	for sale in sales:
# 		sold_stock += sale.total_price
	
# 	for item in stock:
# 		added_stock += item.price

# 	balance = last_opening_stock + added_stock - sold_stock
# 	return balance

def initialize(opening_cash, opening_stock, mback=1, profit=0):
	""" Initialize a business month with set cash and stock values"""

	# Last month
	m = date.today().month - mback
	y = date.today().year
	if m == 0:
		m = 12
		y -= 1

	pdate = date(y, m, 1)
	month = BussinessMonth()

	closing_cash = opening_cash
	closing_stock = opening_stock
	# Backdate by month
	closing_date = pdate
	

	month.opening_cash  = opening_cash
	month.opening_stock = opening_stock
	# month.closing_cash  = closing_cash
	# month.closing_stock = closing_stock

	month.closing_cash = month.balance_cash()
	month.closing_stock = month.balance_stock()
	month.closing_date  = closing_date
	month.profit        = profit

	month.save()
	month.opening_date  = closing_date
	month.save()


# def prep_month():
# 	""" Prepare the bussiness month"""

# 	months = BussinessMonth.objects.all()
# 	if not months.filter(opening_date__month=date.today().month):
# 			last_month.close()
			
# 			this_month = BussinessMonth()
# 			this_month.opening_cash = last_month.closing_cash
# 			this_month.opening_stock = last_month.closing_stock
# 			this_month.save()
# 		else:
# 			this_month = months.filter(opening_date__month=date.today().month)[0]

# 		month_view = {
# 			"last_opening_cash": last_month.opening_cash,
# 			"last_opening_stock": last_month.opening_stock,
# 			"last_closing_cash": last_month.closing_cash,
# 			"last_closing_stock": last_month.closing_stock,
# 			"last_profit": last_month.profit
# 			}
# 		return render(request, "books/viewbussinessmonth.html", {"view": month_view})