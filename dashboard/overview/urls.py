from django.urls import path

from . import views

urlpatterns = [
        path('', views.i_exist, name='i_exist')
]
