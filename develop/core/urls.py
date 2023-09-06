
from django.urls import path, re_path
from core import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='core-index'),
]
