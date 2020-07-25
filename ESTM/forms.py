#Yoe
from django import forms
from .models import ESTM_object
from .models import GRANT_object

class ESTMForm(forms.ModelForm):  # Yoe, This is used to fill the model opbect through the form
	class Meta:
		model = ESTM_object
		fields = ('project_name', 'xyz_file', 'charge', 'multiplicity', 'basis_set', 'num_states', 'selected_state')
		labels = {'project_name': 'Project Name', 'xyz_file': 'Coordinates File (xyz)', 
					'multiplicity': 'Multiplicity (2S+1)', 'basis_set': 'Basis set', 
					'num_states': 'Number of states to compute', 'selected_state': 'State to compute the ESTM'}

class GRANTForm(forms.ModelForm):  # Yoe, This is used to fill the model opbect through the form
	class Meta:
		model = GRANT_object
		fields = ('full_name', 'institution', 'comment')
		labels = {'full_name': 'Full Name', 'institution': 'Name of your institution', 
					'comment': 'Optional Comment (200 characters)'}