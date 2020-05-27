from django.db import models
from django.conf import settings

# Create your models here.

BASIS_SET = (
    ('STO-3G','STO-3G'),
    ('3-21G','3-21G'),
    ('6-31G','6-31G'),
    ('6-31+G*','6-31+G*'),
    ('6-31++G**','6-31++G**'),
    ('6-311G','6-311G'),
    ('6-311+G*','6-311+G*'),
    ('6-311++G**','6-311++G**'),
    ('cc-pVDZ','cc-pVDZ'),
    ('cc-pVTZ','cc-pVTZ'),  
    ('aug-cc-pVDZ','aug-cc-pVDZ'),
    ('aug-cc-pVTZ','aug-cc-pVTZ'),  
)

class ESTM_object(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	project_name = models.CharField(max_length=50) #, primary_key=True) #, unique=True)
	xyz_file = models.FileField(upload_to='xyzfiles/')
	charge = models.IntegerField(default=0)
	multiplicity = models.IntegerField(default=1)
	basis_set = models.CharField(max_length=11, choices=BASIS_SET, default='STO-3G')
	num_states = models.IntegerField(default=6)
	selected_state = models.IntegerField(default=1)
	class Meta:
#		unique_together = ['owner', 'project_name']
		constraints = [
			models.UniqueConstraint(fields=['owner', 'project_name'], name='same_project_name')
			]