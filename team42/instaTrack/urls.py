from django.conf.urls import url

from . import views


app_name = 'instaTrack'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    # e.g: /instaTrack/register/
    url(r'^register/$', views.register, name='register'),
    # e.g: /instaTrack/login/
    url(r'^login/$', views.user_login, name='user_login'),
    # e.g: /instaTrack/logout/
    url(r'^logout/$', views.user_logout, name='user_logout'),

    url(r'^test/?$', views.test, name='test'),

    url(r'^app/.*$', views.app, name='app'),

    url(r'^about/.*$', views.about, name='about')
]
