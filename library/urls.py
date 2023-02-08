from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='library_index'),
    # Reading Clubs
    path('reading-clubs/', include([
        path('', views.reading_clubs, name='reading_clubs'),
        path('create/', views.create_reading_club, name='create_reading_club'),
        path('<int:reading_club_id>/', views.reading_club, name='reading_club'),
        # Sessions
        path('<int:reading_club_id>/sessions/', include([
            path('create/', views.create_reading_club_session, name='create_reading_club_session'),
            path('<int:reading_club_session_id>/', views.reading_club_session, name='reading_club_session'),
        ])),
    ])),
]