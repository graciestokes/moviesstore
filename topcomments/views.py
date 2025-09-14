from django.shortcuts import render
from movies.models import Movie, Review
from django.db.models import Count

def index(request):
    top_reviews = (
        Review.objects
        .annotate(num_likes=Count('likes'))
        .order_by('-num_likes')[:10]
    )
    template_data = {"top_reviews": top_reviews}
    return render(request, 'topcomments/index.html', {'template_data': template_data})

def show(request, id):
    return render(request, 'topcomments/show.html', {'template_data': template_data})
    

