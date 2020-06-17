from django.db import models
from django.conf import settings

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # we use instance instead of request in models
    return '{0}/{1}/{2}/{3}'.format('archive', instance.owner.username, instance.project_name, filename)

class ESTM_archive(models.Model):

	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	project_name = models.CharField(max_length=50) #, primary_key=True) #, unique=True)
	mol2_file = models.FileField(upload_to=user_directory_path)
	xyz_file = models.FileField(upload_to=user_directory_path)
	charge = models.IntegerField(default=0)
	multiplicity = models.IntegerField(default=1)
	basis_set = models.CharField(max_length=50)
	num_states = models.IntegerField(default=6)
	selected_state = models.IntegerField(default=1)
	class Meta:
#		unique_together = ['owner', 'project_name']
		constraints = [
			models.UniqueConstraint(fields=['owner', 'project_name'], name='same_project_name_arch')
			]
