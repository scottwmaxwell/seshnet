from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import DirectChat, DirectMessage

@login_required
def index(request):

	# Get users for Right-navigation panel
	users = User.objects.all()

	# Get direct chats

	context={
		'users': users
	}

	return render(request, 'directmessage/index.html', context)


@login_required
def directmessage(request, dc_id):

	directchat = DirectChat.objects.get(id=dc_id)

	# Check if directchat exists
	if directchat == None:
		return render(request, 'directmessage/error.html')

	# Check if user is a participant in chat
	if request.user not in directchat.participants.all():

		return render(request, 'directmessage/error.html')


	# Get users for Right-navigation panel
	users = User.objects.all()

	# Get last 50 messages
	messages = DirectMessage.objects.filter(directchat=directchat)[::-1][:50][::-1]

	context={
		'users': users,
		'chat_id': dc_id,
		'chat_name': directchat.title,
		'messages': messages
	}


	return render(request, 'directmessage/directmessage.html', context)

@login_required
def get_messages(request, dc_id):
	#TODO
	pass

@login_required
def delete_message(request, dc_id):
	#TODO
	pass

@login_required
def save_image_form(request, dc_id):
	#TODO
	pass

