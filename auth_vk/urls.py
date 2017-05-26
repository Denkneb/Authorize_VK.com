from django.conf.urls import url

from auth_vk import views

urlpatterns = [
    url(r'^$', views.viewLogin, name='login'),
    url(r'^authorize/$', views.authorizeVK, name='authorizeVk'),
    url(r'^profile/$', views.showVK, name='showVK'),
    url(r'^logout/$', views.userLogout, name='userLogout'),
]