from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='library_index'),
    path('livre/<int:livre_id>', views.detail, name='library_detail'),
    path('backoffice', views.backoffice, name='library_backoffice'),
]