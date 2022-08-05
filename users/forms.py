from django import forms
from .models import PharmacyStaff

class PharmacyStaffForm(forms.ModelForm):
	class Meta:
		model = PharmacyStaff
		fields = ["first_name", "last_name", "email", "phone_number", "account_number"]
