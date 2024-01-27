""" Backdate records """
from books.models import Credit, Debit, Stock
from drugs.models import Sale
from datetime import date, datetime

def back(y=0, m=1):
    """ backdate credit, debit, and stock year by y and month by m"""

    credits = Credit.objects.all()
    debits = Debit.objects.all()
    stocks = Stock.objects.all()
    sales = Sale.objects.all()

    # for group in [credits, debits]:
    #     for item in group:
    #         dates = item.book_date
    #         day = dates.day
    #         month = dates.month - m
    #         year = dates.year
    #         if month <= 0:
    #             month += 12
    #             year -= 1
    #         year -= y

    #         new_date = date(year, month, day)
    #         # item.update(book_date=new_date)
    #         item.book_date = new_date
    #         item.save()

    for sale in sales:
        dates = sale.sale_time
        day = dates.day
        month = dates.month - m
        year = dates.year
        if month <= 0:
            month += 12
            year -= 1
        year -= y
        hour = dates.hour
        minute = dates.minute
        second = dates.second
        microsecond = dates.microsecond
        tzinfo = dates.tzinfo

        new_date = datetime(year, month, day, hour, minute, second, microsecond, tzinfo)
        # sale.update(sale_time=new_date)
        sale.sale_time = new_date
        sale.save()


    # for stock in stocks:
    #     pk = stock.pk
    #     dates = stock.date_added
    #     day = dates.day
    #     month = dates.month - m
    #     year = dates.year
    #     if month <= 0:
    #         month += 12
    #         year -= 1
    #     year -= y

    #     new_date = date(year, month, day)
    #     stock = Stock.objects.filter(pk=pk)
    #     stock.update(date_added=new_date)
