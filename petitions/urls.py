from django.urls import path
from . import views
urlpatterns = [
    # Defining a _____/______/ path, which will execute the ______ function defined in the views file
    path('', views.index, name='petitions.index'),
    path('petiton/create/', views.create_petition, name='petitions.create_petition'),
    path('petition/<int:petition_id>/delete/', views.delete_petition, name='petitions.delete_petition'),
    #like url
    path('petition/<int:petition_id>/upvote/', views.upvote_petition, name='petitions.upvote_petition'),
]