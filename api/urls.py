from django.conf.urls import url
from . import views

urlpatterns = [
    url('token$', views.AuthView.as_view(), name='auth_token'),
    url(r'article$', views.HelloView.as_view(), name='hello'),
]
