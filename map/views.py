from django.shortcuts import render
from cart.models import Item
import json

def index(request):
    template_data = {}
    template_data['title'] = 'Local Popularity Map'

    items_query = Item.objects.all()
    items = []
    for item in items_query:
        items.append({
            'img_url': item.movie.image.url,
            'name': item.movie.name,
            'latitude': item.order.user.profile.latitude,
            'longitude': item.order.user.profile.longitude
        })
    template_data['items'] = json.dumps(items)

    return render(request, 'map/index.html', {'template_data': template_data})
