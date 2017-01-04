from django.conf.urls import url

from . import views

app_name = 'classification'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^analysis$', views.analysis, name='analysis'),
]
