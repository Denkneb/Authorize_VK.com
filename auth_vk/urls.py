from django.conf.urls import url, include

from auth_vk import views
# from auth_vk.views import LoginView

urlpatterns = [
    url(r'^$', views.viewLogin, name='login'),
    url(r'^authorize/$', views.authorizeVK, name='authorizeVk'),
    url(r'^profile/$', views.showVK, name='showVK'),
]