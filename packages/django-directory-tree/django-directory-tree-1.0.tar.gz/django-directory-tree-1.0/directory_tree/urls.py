from django.urls import path
from . import views

urlpatterns = [
    path('', views.DirectoryTreeView.as_view(), name='directory_tree'),
]
