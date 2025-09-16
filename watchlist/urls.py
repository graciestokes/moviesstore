from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='watchlist.index'),
    path('<int:id>/', views.show, name='movieswatchlist.show'),
]