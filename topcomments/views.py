from django.shortcuts import render
from movies.models import Movie, Review
from django.db.models import Count
from django.contrib.auth.models import User

def index(request):
    top_reviews = (
        Review.objects
        .annotate(num_likes=Count('likes'))
        .order_by('-num_likes')[:10]
    )
    template_data = {"top_reviews": top_reviews}

    top_users = (
        User.objects
        .annotate(total_likes=Count('review__likes'))
        .order_by('-total_likes')[:10]
    )

    template_data = {
        "top_reviews": top_reviews,
        "top_users": top_users,
    }
    return render(request, 'topcomments/index.html', {'template_data': template_data})
    

