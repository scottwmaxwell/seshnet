from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from .models import Net, Message
from users import views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UploadImageMessage, CreateNet, DeleteNet
from directmessage.forms import CreateDirectChat
from directmessage.models import DirectChat
from django.http import JsonResponse
from users.models import ServerSettings
import datetime
import os

def home(request):

	serversettings = None

	# Check if sever settings exist
	if ServerSettings.objects.all():
		serversettings = ServerSettings.objects.all()[0]

	context = {
		'serversettings': serversettings
	}

	return render(request, 'nets/home.html', context)

@login_required
def index(request):

	if request.method == 'POST':

		form = CreateNet(request.POST)
		if form.is_valid():

			# Check is current user is admin
			if request.user.profile.role == "Admin":
				form.save()


		form = CreateDirectChat(request.POST, request.FILES)
		if form.is_valid():
			if request.POST.get('createchat'):

				user_id = int(request.POST.get('createchat'))
				
				if not DirectChat.objects.filter(participants=(user_id)).filter(participants=(request.user.id)):

					directchat = DirectChat(title="test")
					directchat.save()

					directchat.participants.set((User.objects.get(id=user_id), request.user))

					return redirect('/directmessage/' + str(directchat.id))
				else:

					chat = DirectChat.objects.filter(participants=(user_id)).filter(participants=(request.user.id))[0]

					return redirect('/directmessage/' + str(chat.id))

	createnet_form = CreateNet

	nets = Net.objects.all()
	users = User.objects.all()

	context = {
		'nets': nets,
		'users': users,
		'createnet_form': createnet_form

	}
	return render(request, 'nets/index.html', context)


@login_required
def net(request, net_id):

	if request.method == 'POST':

		form = CreateNet(request.POST)
		if form.is_valid():

			# Check is current user is admin
			if request.user.profile.role == "Admin" or request.user.profile.role == "Moderator":
				form.save()

		form = DeleteNet(request.POST)
		if form.is_valid():
			if request.POST.get('net_id'):
				if request.user.profile.role == "Admin" or request.user.profile.role == "Moderator":
					net_to_delete = Net.objects.get(id=net_id)
					net_to_delete.delete()

					return redirect('net_index')


		form = CreateDirectChat(request.POST, request.FILES)
		if form.is_valid():
			if request.POST.get('createchat'):

				user_id = int(request.POST.get('createchat'))
				
				if not DirectChat.objects.filter(participants=(user_id)).filter(participants=(request.user.id)):

					directchat = DirectChat(title="test")
					directchat.save()

					directchat.participants.set((User.objects.get(id=user_id), request.user))

					return redirect('/directmessage/' + str(directchat.id))
				else:

					chat = DirectChat.objects.filter(participants=(user_id)).filter(participants=(request.user.id))[0]

					return redirect('/directmessage/' + str(chat.id))


	form = UploadImageMessage
	nets = Net.objects.all() # This is for the navbar
	createnet_form = CreateNet
	users = User.objects.all()

	deletenet_form = DeleteNet

	# Get last 50 messages
	messages = Message.objects.filter(net=Net.objects.get(id=net_id))[::-1][:50][::-1]

	context = {
		'net_id': net_id,
		'net_name': Net.objects.get(id=net_id).title,
		'messages': messages,
		'users': users,
		'nets': nets,
		'form': form,
		'createnet_form': createnet_form,
		'deletenet_form': deletenet_form,
	}

	return render(request, 'nets/net.html', context)

@login_required
def get_messages(request, net_id):
	
	if request.method == 'GET':
		
		messageID = request.GET.get('messageID', None)
		
		# get 50 more messages starting from the provided messageID
		messages = Message.objects.filter(id__lte=messageID, net=Net.objects.get(id=net_id))[::-1][:20][1:]
	
		# print("\n\n\n\n LENGTH: ",len(messages))

		if len(messages):
			JsonResponse({"status":"no messages"})

		message_data = {}

		count = 0
		for message in messages:

			date = message.date_sent

			# Month
			date_sent = date.strftime("%B ")

			# Day + Year
			day_year = date.strftime("%d, %Y, ")

			if day_year[0] == "0":
			    day_year = day_year[1:]
			    
			date_sent += day_year

			# Hour
			hour = date.strftime("%H:%M")
			if hour[0] == "0":
			    hour = hour[1:]
			date_sent += hour + ' '

			# AM/PM  
			date_sent += date.strftime('%p').lower().replace("", ".")[1:]


			if message.image:

				message_data[count] = {"message_id": message.id,
									   "message":    message.content,
									   "image_url":  message.image.url,
									   "user":       message.author.username,
									   "date_sent":  date_sent,
									   "pf_pic_url": message.author.profile.image.url
									   }
			else:
				message_data[count] = {"message_id": message.id,
							           "message":    message.content,
							           "image_url":  None,
							           "user":       message.author.username,
							           "date_sent":  date_sent,
							           "pf_pic_url": message.author.profile.image.url
									   }
			count += 1

		return JsonResponse(message_data)
	return JsonResponse({"status":"fail"})

@login_required
def delete_message(request, net_id):

	messageID = request.GET.get('messageID', None)

	message_to_delete = Message.objects.get(id=messageID)

	# Extra check to ensure the person deleting the message is the author, admin, or moderator
	if request.user == message_to_delete.author or request.user.profile.role == 'Admin' or request.user.profile.role == 'Moderator':

		# Delete the message
		message_to_delete.delete()

		return JsonResponse({"status": "success"})
	else:
		return JsonResponse({"status": "fail"})

@login_required
def save_image_form(request, net_id):
	if request.method == 'POST':
		form = UploadImageMessage(request.POST, request.FILES)
		if form.is_valid():

			# I might want to check if it's ajax request too...

			data = {"status": "valid", 
			        "content": form.cleaned_data["content"], 
			        "image": form.cleaned_data["image"]}


			data['content'] = data['content'].replace("<div>","")
			data['content'] = data['content'].replace("</div>","")
			data['content'] = data['content'].replace("<br>","\n")


			# Create a Message with the data...
			message = Message(net=Net.objects.get(id=net_id),
						      author=request.user,
						      date_sent = datetime.datetime.now(),
						      content = data['content'],
							  image = data['image'])


			# Let's save it to the database!
			message.save()

			# Let's return this data so that we can send it to the websocket!

			# Modify date time to match how it's displayed

			# Get date...
			date = message.date_sent

			# Month
			date_sent = date.strftime("%B ")

			# Day + Year
			day_year = date.strftime("%d, %Y, ")

			if day_year[0] == "0":
			    day_year = day_year[1:]
			    
			date_sent += day_year

			# Hour
			hour = date.strftime("%H:%M")
			if hour[0] == "0":
			    hour = hour[1:]
			date_sent += hour + ' '

			# AM/PM  
			date_sent += date.strftime('%p').lower().replace("", ".")[1:]



			data = {
					"status":"valid",
				    "message":message.content,
				    "date_sent": date_sent,
				    "message":message.content,
				    "image_url":message.image.url,
				    "user": message.author.id,
				    "message_id": message.id
					}

		else:
			data={"status":"invalid"}


		return JsonResponse(data)
	