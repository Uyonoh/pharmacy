from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import AdminUser, AppUser, PharmacyStaff
from .forms import AppUserForm, PharmacyStaffForm

# Create your views here.

def register(request):
	form = PharmacyStaffForm()
	print(request)
	if request.method == "POST":
		print(request.POST)
		form = PharmacyStaffForm(request.POST)

		#if the data is valid create a new usew and account
		if form.is_valid:	
			user = create_user(request)
			form.instance.user_id = user.id	
			#form.password = user.password
			print(form.instance.password)
			print("================")
			# print(form.password)
			print(form)
			form.save()	
			# return render(request, "users/register.html", {"form": form})
			return HttpResponseRedirect("/users/login")
		else:
			#print(form.errors)
			return render(request, "users/register.html", {"form": form})
	else:
		return render(request, "users/register.html", {"form": form})

def success(request):
	return render(request, "/users/login.html", {})

def create_user(request):
	username = request.POST.get("first_name")
	print(username)
	print("+++++")
	print()
	password = request.POST.get("password")
	user = User(username=username)
	user.set_password(password)
	user.save()

	return user

def new_form(request):
	form = AppUserForm()
	return render(request, "users/register.html", {"form": form})