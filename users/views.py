from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import AdminUser, PharmacyStaff
from .forms import PharmacyStaffForm

# Create your views here.

def register(request):
	form = PharmacyStaffForm()
	if request.method == "POST":
		print(request.POST)
		form = PharmacyStaffForm(request.POST)

		#if the data is valid create a new usew and account
		if form.is_valid:	
			user = create_user(request)
			form.instance.user_id = user.id	
			form.save()	
			return HttpResponseRedirect("users/success.html")
		else:
			#print(form.errors)
			return render(request, "users/register.html", {"form": form})
	else:
		return render(request, "users/register.html", {"form": form})

def success(request):
	return render(request, "users/success.html", {})

def create_user(request):
	username = request.POST.get("first_name")
	print(username)
	print("+++++")
	print()
	password = "openup"
	user = User(username=username, password=password)
	user.save()

	return user