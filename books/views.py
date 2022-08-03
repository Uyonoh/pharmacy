from datetime import date
from django.shortcuts import render
from books.models import BussinessMonth, Credit, Debit, Stock
from drugs.models import Sale
from .forms import BussinessMonthForm

# Create your views here.

def newbussinessmonth(request):
	months = BussinessMonth.objects.all()
	if not months.count():
		form = BussinessMonthForm(request.POST)
		if form.is_valid():
			form.save()
		return render(request, "books/newbussinessmonth.html", {"form":form})
	else:
		return render(request, "books/viewbussinessmonth.html", {"dr":2})

def viewbussinessmonth(request):
	if newbussinessmonth(request):
		months = BussinessMonth.objects.all()
		if months.count() == 0:
			err_msg = "There is no record as this is the first bussiness month! Please try next month. "
			return render(request, "books/viewbussinessmonth.html", {"err_msg": err_msg})
		last_month = months.filter(opening_date__month=date.today().month-1)[0]
		last_opening_cash = last_month.opening_cash
		last_opening_stock = last_month.opening_stock
		
		new_cash = balance_cash(last_opening_cash)
		new_stock = balance_stock(last_opening_stock)
		if not months.filter(opening_date__month=date.today().month):
			last_month.closing_cash = new_cash
			last_month.closing_stock = new_stock
			last_month.closing_date = date.today()
			last_month.save()

			this_month = BussinessMonth()
			this_month.opening_cash = new_cash
			this_month.opening_stock = new_stock
			this_month.save()
		else:
			this_month = months.filter(opening_date__month=date.today().month)[0]

		month_view = {
			"last_opening_cash": last_opening_cash,
			"last_opening_stock": last_opening_stock,
			"last_closing_cash": last_month.closing_cash,
			"last_closing_stock": last_month.closing_stock
			}
		return render(request, "books/viewbussinessmonth.html", {"view": month_view})
	return newbussinessmonth(request)	


def balance_cash(last_opening_cash):
	credit = 0
	debit = 0

	credits = Credit.objects.filter(book_date__month=date.today().month-1)
	debits = Debit.objects.filter(book_date__month=date.today().month-1)

	for item in credits:
		credit += item.amount
	
	for item in debits:
		debit += item.amount

	balance = last_opening_cash + credit - debit
	return balance

def balance_stock(last_opening_stock):
	sold_stock = 0
	added_stock = 0

	sales = Sale.objects.filter(sale_time__month=date.today().month-1)
	stock = Stock.objects.all()

	for sale in sales:
		sold_stock += sale.total_price
	
	for item in stock:
		added_stock += item.price

	balance = last_opening_stock + added_stock - sold_stock
	return balance

