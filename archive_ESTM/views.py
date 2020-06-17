from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import archiveForm
from .models import ESTM_archive
from ESTM.models import ESTM_object
from django.db import IntegrityError
from django.shortcuts import render, redirect
import time
import shutil
import os

class ArchiveView(LoginRequiredMixin, TemplateView):
	template_name = "archive_ESTM.html"
	try:
		numESTM = ESTM_archive.objects.count()
		if numESTM > 0:
			def get_context_data(self, **kwargs):
				user = self.request.user
				archivo = ESTM_archive.objects.filter(owner=user)
				context = super(ArchiveView, self).get_context_data(**kwargs)
				context['archivo'] = archivo
				return context
	except:
		pass

class UploadMOL2View(LoginRequiredMixin, TemplateView):
	template_name = "upload_mol2.html"
	form_class = archiveForm

	def get_context_data(self, **kwargs):
		context = super(UploadMOL2View, self).get_context_data(**kwargs)
		context['form'] = self.form_class()
		context['check'] = kwargs['check']
		return context

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			if ESTM_object.objects.filter(project_name=form.cleaned_data['project_name'], owner=request.user).exists():
				return redirect('uploadmol2', check='error')
			else:		
				try:
					ESTM_archive.objects.create(
						mol2_file = request.FILES['mol2_file'],
						xyz_file = request.FILES['xyz_file'],
						owner = request.user,
						project_name = form.cleaned_data['project_name'],
						charge = form.cleaned_data['charge'],
						multiplicity = form.cleaned_data['multiplicity'],
						basis_set = form.cleaned_data['basis_set'],
						num_states = form.cleaned_data['num_states'],
						selected_state = form.cleaned_data['selected_state'],				
						)
				except IntegrityError:  # db constraint User-Project_name
					return redirect('uploadmol2', check='error')

				return redirect('archive')
		else:
			return render(request, self.template_name, {'form': self.form_class(), 'check': 'ok'})

class DeleteArchive(LoginRequiredMixin, TemplateView):
	template_name = 'archive_ESTM.html'

	def get(self, request, **kwargs):
	   #
	   # Remove the ESTM_archive object and the folder:
	   # archive/user/project_name
	   #
		path = ESTM_archive.objects.get(pk=kwargs['job_pk']).xyz_file.path
		dirname, basename = os.path.split(path.rstrip('/'))
		src = dirname
		ESTM_archive.objects.get(pk=kwargs['job_pk']).delete()
		shutil.rmtree(src)
		return redirect('archive')






