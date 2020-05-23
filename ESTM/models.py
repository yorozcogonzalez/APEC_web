from django.db import models
from django.conf import settings

# Create your models here.
class ESTM_object(models.Model):
#	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	project_name = models.CharField(max_length=50, primary_key=True) #, unique=True)
	xyz_file = models.FileField(upload_to='xyzfiles/')
	charge = models.IntegerField(default=0)
	multiplicity = models.IntegerField(default=1)
