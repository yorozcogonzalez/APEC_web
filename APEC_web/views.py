from django.views.generic import TemplateView, DetailView, ListView
from django.conf import settings
from django.http import HttpResponse

from django_remote_submission.models import Interpreter, Server, Job, Log
from django_remote_submission.tasks import submit_job_to_server, copy_file_to_server
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.conf import settings
from ESTM.models import ESTM_object
from archive_ESTM.models import ESTM_archive

import os

import textwrap
import logging
import time

logger = logging.getLogger(__name__)  # pylint: disable=C0103

class HomePageView(TemplateView):
    template_name = "home.html"

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
            #    Yoe. Used to add information to context in addition to the generic TemplateView context.
            #    This is equivalent to: TemplateView.get_context_data(**kwargs)
            #    Since we do not have a defined model for this view, we need to do it in that way.
            #    If we create a model before, there is no need of doing that, see example here:
            #    https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-display/
            #    Adding extra context
        context['job_list'] = Job.objects.all()
        context['server_list'] = Server.objects.all()
        context['Log_list'] = Log.objects.all()
        return context


class ServerDetail(LoginRequiredMixin, DetailView):
    model = Server


class ServerList(LoginRequiredMixin, ListView):
    model = Server


class JobDetail(LoginRequiredMixin, DetailView):
    model = Job


class JobList(LoginRequiredMixin, ListView):
    model = Job


class JobLogView(LoginRequiredMixin, TemplateView):
    template_name = 'job_log.html'

    def get_context_data(self, **kwargs):
        context = super(JobLogView, self).get_context_data(**kwargs)
        context['job_pk'] = kwargs['job_pk']
        state = Job.objects.get(pk=kwargs['job_pk']).state
        status = Job.objects.get(pk=kwargs['job_pk']).status
        context['state'] = state
        context['status'] = status
        return context

class ShowJobs(LoginRequiredMixin, TemplateView):
    template_name = "show_jobs.html"
    def get_context_data(self, **kwargs):
        context = super(ShowJobs, self).get_context_data(**kwargs)
        context['method'] = kwargs['method']
        return context

class mol3dSurfView(LoginRequiredMixin, TemplateView):
    template_name = 'mol3d_surface.html'
#    job_data = Job.objects.get(pk=int(kwargs['job_pk']))
#    url = '/media/results/' + job_data.estm_data.project_name + '/pointsXx.xyz'
    def get_context_data(self, **kwargs):
        context = super(mol3dSurfView, self).get_context_data(**kwargs)
        job_data = Job.objects.get(pk=int(kwargs['job_pk']))
        url = settings.MEDIA_URL + 'results/' + job_data.owner.username + '/' + job_data.estm_data.project_name + '/pointsXx.xyz'
        urlpath = settings.MEDIA_ROOT + 'results/' + job_data.owner.username + '/' + job_data.estm_data.project_name + '/pointsXx.xyz'
        urlmolecule = job_data.estm_data.xyz_file.url
        check = os.path.exists(urlpath)
        while not check:
            time.sleep(1)
            check = os.path.exists(urlpath)

        context['url'] = url
        context['urlmolecule'] = urlmolecule
        context['job_pk'] = kwargs['job_pk']
        context['state'] = job_data.state
        return context

class mol3dESTMView(LoginRequiredMixin, TemplateView):
    template_name = 'mol3d_estm.html'
#    job_data = Job.objects.get(pk=int(kwargs['job_pk']))
#    url = '/media/results/' + job_data.estm_data.project_name + '/pointsXx.xyz'
    def get_context_data(self, **kwargs):
        context = super(mol3dESTMView, self).get_context_data(**kwargs)
        fromm = kwargs['fromm']
        if fromm == 'job':
            job_data = Job.objects.get(pk=int(kwargs['job_pk']))
            project_name = job_data.estm_data.project_name
            urlmol2 = settings.MEDIA_URL + 'results/' + job_data.owner.username + '/' + project_name + '/' + project_name + '.mol2'
            urlxyz = settings.MEDIA_URL + 'results/' + job_data.owner.username + '/' + project_name + '/' + project_name + '.xyz'
        elif fromm == 'archive':
            archive_data = ESTM_archive.objects.get(pk=int(kwargs['job_pk']))
            urlmol2 = archive_data.mol2_file.url
            urlxyz = archive_data.xyz_file.url
        limit = 1.0

        context['urlmol2'] = urlmol2
        context['urlxyz'] = urlxyz
        context['job_pk'] = kwargs['job_pk']
        context['lim'] = limit
        return context

class TutorialView(TemplateView):
    template_name = "tutorial_video.html"

class Inprogress(LoginRequiredMixin, TemplateView):
    template_name = "In_progress.html"




    
