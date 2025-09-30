from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('requests/create/', views.create_movie_request, name='movies.create_request'),
    path('requests/<int:req_id>/delete/', views.delete_movie_request, name='movies.delete_request'),
    path("petition/", views.petition_index, name="movies.petition.petition_index"),
    path("petition/create/", views.create_petition, name="movies.petition.create"),
    path("petition/<int:pk>/vote/yes/", views.vote_yes, name="movies.petition.vote_yes"),
    path("petition/<int:pk>/vote/unvote/", views.unvote, name="movies.petition.unvote"),
]