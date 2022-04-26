from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from .models import Net, Message
from users import views
from django.contrib.auth.decorators import login_required


def home(request):

	return render(request, 'nets/home.html')


def index(request):

	nets = Net.objects.all()

	context = {
		'nets': nets,
	}

	return render(request, 'nets/index.html', context)

def net(request, net_id):

	nets = Net.objects.all()

	messages = Message.objects.filter(net=Net.objects.get(id=net_id))

	context = {
		'net_id': net_id,
		'net_name': Net.objects.get(id=net_id).title,
		'messages': messages,
		'nets': nets,
	}

	return render(request, 'nets/net.html', context)