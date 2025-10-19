from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User #import the User model from Django’s authentication system.
from .models import Profile 

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['username'], password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required #ensure that the user must be logged in to access the orders function.
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders' #define the template_data variable and assign it a title.
    template_data['orders'] = request.user.order_set.all() #We retrieve all orders belonging to the currently logged-in user (request.user). The order_set attribute is used to access the related orders associated with the user through their relationship
    return render(request, 'accounts/orders.html', {'template_data': template_data}) #pass the orders to the template and render it

@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile.latitude = request.POST.get('latitude')
        profile.longitude = request.POST.get('longitude')
        profile.save()
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'profile': profile})
