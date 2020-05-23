#Yoe
from django import forms
from .models import ESTM_object

class ESTMForm(forms.ModelForm):  # Yoe, This is used to fill the model opbect through the form
	class Meta:
		model = ESTM_object
		fields = ('project_name', 'xyz_file', 'charge', 'multiplicity')
		labels = {'project_name': 'Project Name', 'xyz_file': 'Coordinates File (xyz)', 
					'multiplicity': 'Multiplicity (2S+1)'}