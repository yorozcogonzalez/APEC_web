#Yoe
from django import forms
from .models import ESTM_object

class ESTMForm(forms.ModelForm):  # Yoe, This is used to fill the model opbect through the form
	class Meta:
		model = ESTM_object
		fields = ('project_name', 'xyz_file', 'charge', 'multiplicity', 'basis_set', 'num_states', 'selected_state')
		labels = {'project_name': 'Project Name', 'xyz_file': 'Coordinates File (xyz)', 
					'multiplicity': 'Multiplicity (2S+1)', 'basis_set': 'Basis set', 
					'num_states': 'Number of states to compute', 'selected_state': 'State to compute the ESTM'}