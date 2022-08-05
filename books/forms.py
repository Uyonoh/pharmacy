from django import forms
from .models import BussinessMonth

class BussinessMonthForm(forms.ModelForm):
	class Meta:
		model = BussinessMonth
		fields = ["opening_cash", "opening_stock"]	