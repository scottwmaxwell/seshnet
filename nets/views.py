from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from .models import Net, Message
from users import views
from django.contrib.auth.decorators import login_required


def home(request):

	if request.user.is_authenticated:
		return render(request, 'nets/home.html')
	else:
		return render(request, 'nets/home-unathenticated.html')

def net(request, net_id):

	# if request.method == 'POST':
	# 	form = SendMessage(request.POST, request.FILES)
	# 	if form.is_valid():
	# 		message = form.save(commit=False)
	# 		message.net = Net.objects.get(id=net_id)
	# 		message.author = request.user
	# 		message.save()

	messages = Message.objects.filter(net=Net.objects.get(id=net_id))

	context = {
		'net_id': net_id,
		'net_name': Net.objects.get(id=net_id).title,
		'messages': messages
	}

	return render(request, 'nets/net.html', context)