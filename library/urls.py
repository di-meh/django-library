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
            path('<int:reading_club_session_id>/', include([
                path('join/', views.join_reading_club_session, name='join_reading_club_session'),
                path('leave/', views.leave_reading_club_session, name='leave_reading_club_session'),
            ])),
        ])),
    ])),
    path('livre/<int:livre_id>', views.detail, name='library_detail'),
    path('backoffice', views.backoffice, name='library_backoffice'),
]