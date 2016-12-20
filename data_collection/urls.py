from django.conf.urls import url

from . import views

app_name = 'data_collection'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^showcase$', views.showcase_urls, name='showcase')
]
