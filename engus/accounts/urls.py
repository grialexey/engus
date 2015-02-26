from django.conf.urls import patterns, include, url
from .views import ProfileView


urlpatterns = patterns('',
    url('^profile/$', ProfileView.as_view(), name='profile'),
)
