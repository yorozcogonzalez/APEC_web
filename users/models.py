from django.contrib.auth.models import AbstractUser # Yoe

class CustomUser(AbstractUser):
	# add additional fields in here

	def __str__(self):
		return self.email