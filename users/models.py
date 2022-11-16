from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.db.models.deletion import CASCADE

# Create your models here.

class AppUser(AbstractBaseUser):
	""" Base user model """
	user = models.OneToOneField(User, to_field="id", null=False, blank=False, on_delete=CASCADE)
	first_name = models.CharField(max_length=50, null=False)
	last_name = models.CharField(max_length=50, null=True)
	middle_name = models.CharField(max_length=50, null=True, blank=False)
	email = models.EmailField(null=True)
	phone_number = models.IntegerField(null=True, blank=False)

	USERNAME_FIELD = "email"
	EMAIL_FIELD = "email"
	REQUIRED_FIELDS = ["first_name", "last_name"]

	objects = BaseUserManager()

	# def set_password(self, raw_password):
	# 	""" Encrypt password """
	# 	self.password = make_password(raw_password)

	def save(self):
		self.set_password(self.password)
		super().save()

class BaseUserAccount(models.Model):
	""" ExBase user model """
	user = models.OneToOneField(User, to_field="id", null=False, blank=False, on_delete=CASCADE)
	first_name = models.CharField(max_length=50, null=False)
	last_name = models.CharField(max_length=50, null=True)
	middle_name = models.CharField(max_length=50, null=True)
	email = models.EmailField(null=True)
	phone_number = models.IntegerField(null=True)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'

	def login(self, raw_password):
		return check_password(raw_password, self.user.password)

	def name(self):
		self.__str__()
	
	def set_password(self, raw_password):
		""" Encrypt password """
		self.password = make_password(raw_password)


class AdminUser(AppUser):
	User.is_superuser = True
	root_token = models.CharField(max_length=200, null=True, blank=True)

class PharmacyStaff(AppUser):
	account_number = models.IntegerField(null=True)
	admin_token = models.CharField(max_length=200, null=True)

