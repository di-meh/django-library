from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='library_index'),
    path('reading-clubs/', views.reading_clubs, name='reading_clubs'),
    path('reading-clubs/create/', views.create_reading_club, name='create_reading_club'),
]