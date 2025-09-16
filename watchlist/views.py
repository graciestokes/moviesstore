from django.shortcuts import render, redirect, get_object_or_404
from movies.models import Movie, Review
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
        for movie in movies:
            if not request.user in movie.watch_listed_movies.all:
                movies.remove(movie)
    else:
        movies = request.user.watch_listed_movies.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'watchlist/index.html', {'template_data': template_data})

@login_required
def show(request, id):
    return redirect('movies.show', id=id)