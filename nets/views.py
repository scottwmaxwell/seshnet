from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from users import views
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):

	if request.user.is_authenticated:
		return render(request, 'nets/home.html')
	else:
		return render(request, 'nets/home-unathenticated.html')