"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from django.urls import path, include

from APEC_web import views
from ESTM import views as estmviews

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^index$', views.IndexView.as_view(), name='index'),

    url(r'^logs/(?P<job_pk>[0-9]+)/$', views.JobLogView.as_view(), name='logs'),
    url(r'^servers/$', views.ServerList.as_view(), name='server-list'),
    url(r'^servers/(?P<pk>[0-9]+)/$', views.ServerDetail.as_view(), name='server-detail'),
    url(r'^jobs/$', views.JobList.as_view(), name='job-list'),
    url(r'^api/', include('django_remote_submission.urls')),
    url(r'^method/(?P<method>\w+)/$', views.ShowJobs.as_view(), name='method'),
    url(r'^estmform/(?P<check>\w+)/$', estmviews.ESTM_View.as_view(), name='ESTM'),
    url(r'^estmform/(?P<check>\w+)/$', estmviews.ESTM_View.as_view(), name='APEC'),
    url(r'^estmform/(?P<check>\w+)/$', estmviews.ESTM_View.as_view(), name='FEG'),
    url(r'^3dmolSurf/(?P<job_pk>[0-9]+)/$', views.mol3dSurfView.as_view(), name='mol3d_surf'),
    url(r'^3dmolESTM/(?P<job_pk>[0-9]+)/$', views.mol3dESTMView.as_view(), name='mol3d_estm'),
    url(r'^ESTM_calc/(?P<job_pk>[0-9]+)/$', estmviews.ESTM_Calculation.as_view(), name='ESTM_calc'),
    url(r'^delete/(?P<job_pk>[0-9]+)/$', estmviews.DeleteJobView.as_view(), name='delete'),

   # Login Yoe
    path('admin/', admin.site.urls),
    path('users/', include('allauth.urls')),
    path('', views.HomePageView.as_view(), name='home'),

]

# Serving files uploaded by a user during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
