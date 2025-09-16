from django.shortcuts import render, get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    movie = get_object_or_404(Movie, id=id)
    requested_quantity = int(request.POST['quantity'])
    
    # Check if enough stock is available
    if movie.amount_left < requested_quantity:
        messages.error(request, f'Sorry, only {movie.amount_left} copies of "{movie.name}" are available.')
        return redirect('movies.show', id=id)
    
    cart = request.session.get('cart', {})
    
    # Check if item already in cart
    current_cart_quantity = int(cart.get(str(id), 0))
    total_requested = current_cart_quantity + requested_quantity
    
    if movie.amount_left < total_requested:
        available = movie.amount_left - current_cart_quantity
        if available <= 0:
            messages.error(request, f'"{movie.name}" is already at maximum quantity in your cart.')
        else:
            messages.error(request, f'Only {available} more copies of "{movie.name}" can be added to your cart.')
        return redirect('movies.show', id=id)
    
    cart[str(id)] = str(total_requested)
    request.session['cart'] = cart
    messages.success(request, f'Added {requested_quantity} copies of "{movie.name}" to your cart.')
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    
    # Check stock availability before processing purchase
    for movie in movies_in_cart:
        requested_quantity = int(cart[str(movie.id)])
        if movie.amount_left < requested_quantity:
            messages.error(request, f'Sorry, only {movie.amount_left} copies of "{movie.name}" are available. Please update your cart.')
            return redirect('cart.index')
    
    cart_total = calculate_cart_total(cart, movies_in_cart)
    
    # Create order
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    
    # Process each movie and update inventory
    for movie in movies_in_cart:
        quantity = int(cart[str(movie.id)])
        
        # Create order item
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = quantity
        item.save()
        
        # Decrease movie inventory
        movie.amount_left -= quantity
        movie.save()
    
    # Clear cart
    request.session['cart'] = {}
    
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    
    messages.success(request, 'Purchase completed successfully!')
    return render(request, 'cart/purchase.html', {'template_data': template_data})