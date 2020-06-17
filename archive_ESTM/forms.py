#Yoe
from django import forms
from .models import ESTM_archive

class archiveForm(forms.ModelForm):  # Yoe, This is used to fill the model opbect through the form
	class Meta:
		model = ESTM_archive
		fields = ('project_name', 'mol2_file', 'xyz_file', 'charge', 'multiplicity', 'basis_set', 'num_states', 'selected_state')
		labels = {'project_name': 'Project Name', 'mol2_file': 'Mol2 File', 'xyz_file': 'xyz File',
					'multiplicity': 'Multiplicity (2S+1)', 'basis_set': 'Basis set', 
					'num_states': 'Number of states to compute', 'selected_state': 'State to compute the ESTM'}