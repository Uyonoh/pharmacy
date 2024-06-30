from django import forms
# from matplotlib import widgets
from .models import PharmacyStaff, AppUser

class PharmacyStaffForm(forms.ModelForm):
	class Meta:
		model = PharmacyStaff
		fields = ["first_name", "last_name", "phone_number", "account_number", "email", "password"]
		widgets = {"password": forms.PasswordInput()}

class AppUserForm(forms.ModelForm):
	class Meta:
		model = AppUser
		fields = ["first_name", "last_name", "phone_number", "email", "password"]
		widgets = {"password": forms.PasswordInput()}