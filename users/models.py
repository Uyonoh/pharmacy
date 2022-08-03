from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class AdminUser(models.Model):
	User.is_superuser = True
	user = models.ForeignKey(User, null=False, blank=False, on_delete=CASCADE)
	first_name = models.CharField(max_length=50, null=False)
	last_name = models.CharField(max_length=50, null=False)
	middle_name = models.CharField(max_length=50, null=True)
	email = models.EmailField(null=False)
	phone_number = models.IntegerField()
	root_token = models.CharField(max_length=200)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'

	def name(self):
		self.__str__()
