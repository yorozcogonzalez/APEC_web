from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import ESTMForm
from .models import ESTM_object
from django_remote_submission.models import Interpreter, Server, Job, Log
from django_remote_submission.tasks import submit_job_to_server, copy_file_to_server, delete_jobs_from_server
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.conf import settings
import os
import shutil

import textwrap
import logging
import time

from django.db import IntegrityError

logger = logging.getLogger(__name__)  # pylint: disable=C0103

class ESTM_View(LoginRequiredMixin, TemplateView):
	form_class = ESTMForm
#	success_url = reverse_lazy('submit')
	template_name = 'base_form.html'

	def get_context_data(self, **kwargs):
		context = super(ESTM_View, self).get_context_data(**kwargs)
		context['form'] = self.form_class()
		context['method'] = 'ESTM'
		context['check'] = kwargs['check']
		return context

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			try:
				estm = ESTM_object.objects.create(xyz_file = request.FILES['xyz_file'],
				owner = request.user,
				project_name = form.cleaned_data['project_name'],
				charge = form.cleaned_data['charge'],
				multiplicity = form.cleaned_data['multiplicity'],
				basis_set = form.cleaned_data['basis_set'],
				num_states = form.cleaned_data['num_states'],
				selected_state = form.cleaned_data['selected_state'],				
			)

			except IntegrityError:
				return render(request, self.template_name, {'form': form})				
#			estm.save()

			(interpreter, _) = Interpreter.objects.get_or_create(
				name='bash',
				path='/usr/bin/bash',
				arguments='',
	#            name='Python',
	#            path=settings.PYTHON_PATH,
	#            arguments=settings.PYTHON_ARGUMENTS,
			)
			(server, _) = Server.objects.get_or_create(
				title='Example Server',
				hostname=settings.SERVER_HOSTNAME,
				port=settings.SERVER_PORT,
			)
			logger.debug("Running job in {} using {}".format(server, interpreter))

#			num_estm = len(ESTM_object.objects.all())
#			job_data = ESTM_object.objects.filter()[num_estm-1]
#			filepath = job_data.xyz_file.path
##			filename = job_data.xyz_file.name  # it gives xyzfiles/name
#			dirname, basename = os.path.split(filepath.rstrip('/'))
#			filename = basename
#			project_name = job_data.project_name
#			multiplicity = job_data.multiplicity
#			charge = job_data.charge

			filepath = estm.xyz_file.path
			dirname, basename = os.path.split(filepath.rstrip('/'))
			filename = basename

			program = textwrap.dedent('''\
#!/bin/bash
remote=%s
filename=%s
cp $remote/templates/Infos.dat .
cp $remote/templates/vdw_surface_tp.py vdw_surface.py
cp $remote/templates/ESTM.py .
cp $remote/templates/create_inputs.sh create_inputs_%s.sh
source /home/yoelvis/virtual_envs/vdw_surface/bin/activate

echo Project %s >> Infos.dat
echo xyz_name $filename >> Infos.dat
echo charge %s >> Infos.dat
echo multiplicity %s >> Infos.dat
echo basis_set %s >> Infos.dat
echo num_states %s >> Infos.dat
echo selected_state %s >> Infos.dat
sed -i "s/FILENAME/$filename/" vdw_surface.py
check="no"
if [[ -f $filename ]]; then
	check="yes"
fi
while [[ $check != "yes" ]]; do
    sleep 0.5
	if [[ -f $filename ]]; then
		check="yes"
	fi
done
python vdw_surface.py
	    	''') %(settings.REMOTE_DIRECTORY, filename, estm.project_name, estm.project_name, estm.charge, estm.multiplicity,
	    	estm.basis_set, estm.num_states, estm.selected_state)
			remote_directory = settings.REMOTE_DIRECTORY + '/' + str(request.user.username) + '/' + estm.project_name + '/' 
			(job, _) = Job.objects.get_or_create(
				title=estm.project_name,
				program=program,
				remote_directory=remote_directory,
				remote_filename=settings.REMOTE_FILENAME,
				owner=request.user,
				server=server,
				interpreter=interpreter,
				estm_data=estm
			)

			while not os.path.isfile(job.estm_data.xyz_file.path):
				time.sleep(1)

			copy_file_to_server.delay(
				job_pk=job.pk,
				password=settings.REMOTE_PASSWORD,
				username=settings.REMOTE_USER,
			)
			time.sleep(2)
			submit_job_to_server.delay(     #deley is used by celery to pass task to the queue
				job_pk=job.pk,
				password=settings.REMOTE_PASSWORD,
				username=settings.REMOTE_USER,
			)
			#return render(request, 'test.html', {'test': newdoc}) # Usamos esto si queremos pasarle y ver los resultados en test.html
			#return render(request, 'estm_job_status.html', {'newdoc': newdoc}) # Te redirecciona pero no hace las funciones del view
			return redirect('method', method='ESTM')
		else:
			return redirect('ESTM', check='error')
#			return render(request, self.template_name, {'form': form})

class ESTM_Calculation(LoginRequiredMixin, TemplateView):
	template_name = 'show_jobs.html'
	# Here we use get to get information from the url: kwargs['job_pk']
	def get(self, request, **kwargs):
		job_data = Job.objects.get(pk=kwargs['job_pk'])
		program2 = textwrap.dedent('''\
#!/bin/bash
bash create_inputs_%s.sh
	    ''') %(job_data.title)
		job_data.program = program2
		job_data.state = "vdw"
		job_data.status = "initial"
#		job_data.remote_filename=settings.REMOTE_FILENAMEO,
		job_data.save()

		submit_job_to_server.delay(     #deley is used by celery to pass task to the queue
			job_pk=kwargs['job_pk'],
			password=settings.REMOTE_PASSWORD,
			username=settings.REMOTE_USER,
		)
		return redirect('method', method='ESTM')
#		return render(request, self.template_name, {'method': 'ESTM'})

class DeleteJobView(LoginRequiredMixin, TemplateView):
	template_name = 'show_jobs.html'

	def cancel_prep(self):
		job_data = self.job_data
		project_name = self.project_name
		request = self.request
		kwargs = self.kwargs

		scancel = textwrap.dedent('''\
#!/bin/bash
rm -rf %s
exit 0
		''') %(project_name)

		remote_directory = settings.REMOTE_DIRECTORY + '/' + str(request.user.username) + '/'
		(job, _) = Job.objects.get_or_create(
			title='Deleting_' + project_name,
			program=scancel,
			remote_directory=remote_directory,
			remote_filename='Deleting_' + project_name,
			owner=request.user,
			server=job_data.server,
			interpreter=job_data.interpreter,
			estm_data=None,
		)
		status = Job.objects.get(pk=kwargs['job_pk']).status
		check = False
		while not check:
#testing			if status == 'success' or status == 'failure':
			if status != 'initial':
				check = True
			else:
				status = Job.objects.get(pk=kwargs['job_pk']).status
				time.sleep(1)

		delete_jobs_from_server.delay(     #deley is used by celery to pass task to the queue
			job_pk=job.pk,
			password=settings.REMOTE_PASSWORD,
			username=settings.REMOTE_USER,
		)
		status1 = Job.objects.get(pk=job.pk).status
		check = False
		while not check:
			if status1 == 'success' or status1 == 'failure':
				check = True
			else:
				time.sleep(1)
				status1 = Job.objects.get(pk=job.pk).status

		time.sleep(1)
		ESTM_object.objects.get(project_name = project_name).delete()
		Job.objects.get(title = 'Deleting_' + project_name).delete()

	def cancel_vdw(self):
		job_data = self.job_data
		project_name = self.project_name
		request = self.request
		kwargs = self.kwargs

		scancel = textwrap.dedent('''\
#!/bin/bash
proj="%s"
calculations=`grep "Calculations" $proj/Infos.dat | awk '{ print $2 }'`
if [[ $calculations != "done" ]]; then   
   while [[ $calculations != "submitted" ]]; do
      calculations=`grep "Calculations" $proj/Infos.dat | awk '{ print $2 }'`
      sleep 1
   done

   mv $proj/jobnumbers jobnumbers_$proj

   numjobs=`wc -l jobnumbers_$proj | awk '{ print $1 }'`
   for i in $(seq 1 $numjobs); do
      job=`head -n $i jobnumbers_$proj | tail -n1 | awk '{ print $4 }'`
      scancel $job 2>/dev/null
   done

   while [[ $calculations != "deleted" ]]; do
      calculations=`grep "Calculations" $proj/Infos.dat | awk '{ print $2 }'`
      sleep 1
   done
   rm -r $proj jobnumbers_$proj.sh
#else
#   sleep 1
#   rm -rf $proj
fi
exit 0
		''') %(project_name)
		remote_directory = settings.REMOTE_DIRECTORY + '/' + str(request.user.username) + '/'
		(job, _) = Job.objects.get_or_create(
			title='Deleting_' + project_name,
			program=scancel,
			remote_directory=remote_directory,
			remote_filename='Deleting_' + project_name,
			owner=request.user,
			server=job_data.server,
			interpreter=job_data.interpreter,
			estm_data=None,
		)

		delete_jobs_from_server.delay(     #deley is used by celery to pass task to the queue
			job_pk=job.pk,
			password=settings.REMOTE_PASSWORD,
			username=settings.REMOTE_USER,
		)

		status1 = Job.objects.get(pk=kwargs['job_pk']).status  #original job
		status2 = Job.objects.get(pk=job.pk).status            #deleting job
		check = False
		while not check:
			if (status1 == 'success' or status1 == 'failure') and status2 == 'success':
				check = True
			else:
				status1 = Job.objects.get(pk=kwargs['job_pk']).status
				status2 = Job.objects.get(pk=job.pk).status
				time.sleep(1)

		ESTM_object.objects.get(project_name = project_name).delete()
		Job.objects.get(title = 'Deleting_' + project_name).delete()

	def cancel_fail(self):
		job_data = self.job_data
		project_name = self.project_name
		request = self.request
		kwargs = self.kwargs

		scancel = textwrap.dedent('''\
#!/bin/bash
proj="%s"
if [[ -f $proj/jobnumbers ]]; then   
   mv $proj/jobnumbers jobnumbers_$proj
   numjobs=`wc -l jobnumbers_$proj | awk '{ print $1 }'`
   if [[ $numjobs -gt 0 ]]; then
      for i in $(seq 1 $numjobs); do
         job=`head -n $i jobnumbers_$proj | tail -n1 | awk '{ print $4 }'`
         scancel $job 2>/dev/null
      done
   fi
   sleep 1
   rm -r $proj jobnumbers_$proj.sh
else
   sleep 1
   rm -rf $proj
fi
exit 0
		''') %(project_name)
		remote_directory = settings.REMOTE_DIRECTORY + '/' + str(request.user.username) + '/'
		(job, _) = Job.objects.get_or_create(
			title='Deleting_' + project_name,
			program=scancel,
			remote_directory=remote_directory,
			remote_filename='Deleting_' + project_name,
			owner=request.user,
			server=job_data.server,
			interpreter=job_data.interpreter,
			estm_data=None,
		)

		delete_jobs_from_server.delay(     #deley is used by celery to pass task to the queue
			job_pk=job.pk,
			password=settings.REMOTE_PASSWORD,
			username=settings.REMOTE_USER,
		)

		status1 = Job.objects.get(pk=kwargs['job_pk']).status  #original job
		status2 = Job.objects.get(pk=job.pk).status            #deleting job
		check = False
		while not check:
			if (status1 == 'success' or status1 == 'failure') and status2 == 'success':
				check = True
			else:
				status1 = Job.objects.get(pk=kwargs['job_pk']).status
				status2 = Job.objects.get(pk=job.pk).status
				time.sleep(1)

		ESTM_object.objects.get(project_name = project_name).delete()
		Job.objects.get(pk=job.pk).delete()


	def get(self, request, **kwargs):
		job_data = Job.objects.get(pk=kwargs['job_pk'])
		try:
			project_name = job_data.estm_data.project_name
			self.project_name = project_name
		except:
			pass
		self.job_data = job_data
		self.request = request
		self.kwargs = kwargs

		if job_data.estm_data is None:
			while job_data.status != "success":
				time.sleep(1)
			Job.objects.get(pk=kwargs['job_pk']).delete()
		else:
			if job_data.status != "failure":
				if job_data.state == "prep":
					self.cancel_prep()
				if job_data.state == "vdw":
					self.cancel_vdw()
			else:
				self.cancel_fail()

				


		time.sleep(1)
		try:
			os.remove(job_data.estm_data.xyz_file.path)
		except:
			pass
		path = settings.MEDIA_ROOT + "results/" + job_data.owner.username + "/" + job_data.title
		while os.path.isdir(path):
			try:
				shutil.rmtree(settings.MEDIA_ROOT + "results/" + job_data.owner.username + "/" + job_data.title)
			except:
				pass
			time.sleep(1)

		return redirect('method', method='ESTM')
	


