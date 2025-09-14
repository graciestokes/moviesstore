from django.urls import path
from . import views
urlpatterns = [
    # Defining a _____/______/ path, which will execute the ______ function defined in the views file
    path('', views.index, name='topcomments.index'),
]