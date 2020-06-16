from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('login_get_state', views.login_get_state),
    path('login_verify_get', views.login_verify_get),
    path('login_verify_set', views.login_verify_set),
    path('download', views.download),
    path('download_get_state', views.download_get_state),
    path('update', views.update),
    path('update_get_state', views.update_get_state),
    path('user_list', views.user_list),
]
