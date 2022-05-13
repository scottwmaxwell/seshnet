from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import DirectChat, DirectMessage
from django.http import JsonResponse
from .forms import UploadImageMessage, CreateDirectChat
import datetime

@login_required
def index(request):

	if request.method == "POST":
		
		form = CreateDirectChat(request.POST, request.FILES)
		if form.is_valid():
			if request.POST.get('createchat'):

				user_id = int(request.POST.get('createchat'))
				

				if not DirectChat.objects.filter(participants=(user_id, request.user.id)):

					directchat = DirectChat(title="test")
					directchat.save()

					directchat.participants.set((User.objects.get(id=user_id), request.user))

					return redirect('/directmessage/' + str(directchat.id))
				else:

					chat = DirectChat.objects.filter(participants=(user_id, request.user.id))[0]

					return redirect('/directmessage/' + str(chat.id))




	# Get users for Right-navigation panel
	users = User.objects.all()


	# This form isn't really used... but I use it to validate the CSRF token (see above)...
	createdirectchat = CreateDirectChat

	# Get direct chats
	directchats = DirectChat.objects.filter(participants=request.user)

	context={
		'users': users,
		'directchats': directchats,
		'createdirectchat': createdirectchat,
	}

	return render(request, 'directmessage/index.html', context)


@login_required
def directmessage(request, dc_id):


	if request.method == "POST":
		
		form = CreateDirectChat(request.POST, request.FILES)
		if form.is_valid():
			if request.POST.get('createchat'):

				user_id = int(request.POST.get('createchat'))
				

				if not DirectChat.objects.filter(participants=(user_id, request.user.id)):

					directchat = DirectChat(title="test")
					directchat.save()

					directchat.participants.set((User.objects.get(id=user_id), request.user))

					return redirect('/directmessage/' + str(directchat.id))
				else:

					chat = DirectChat.objects.filter(participants=(user_id, request.user.id))[0]

					return redirect('/directmessage/' + str(chat.id))


	form = UploadImageMessage

	directchat = DirectChat.objects.get(id=dc_id)

	createdirectchat = CreateDirectChat

	# Check if directchat exists
	if directchat == None:
		return render(request, 'directmessage/error.html')

	# Check if user is a participant in chat
	if request.user not in directchat.participants.all():

		return render(request, 'directmessage/error.html')


	# Get users for Right-navigation panel
	users = User.objects.all()

	# Get direct chats
	directchats = DirectChat.objects.filter(participants=request.user)

	# Get last 50 messages
	messages = DirectMessage.objects.filter(directchat=directchat)[::-1][:50][::-1]

	context={
		'users': users,
		'chat_id': dc_id,
		'chat_name': directchat.title,
		'messages': messages,
		'form': form,
		'directchats': directchats,
		'createdirectchat': createdirectchat,
	}


	return render(request, 'directmessage/directmessage.html', context)

@login_required
def get_messages(request, dc_id):

	if request.method == 'GET':
		
		messageID = request.GET.get('messageID', None)
		
		# get 50 more messages starting from the provided messageID
		messages = DirectMessage.objects.filter(id__lte=messageID, directchat=DirectChat.objects.get(id=dc_id))[::-1][:20][1:]

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
def delete_message(request, dc_id):

	print('hello')

	messageID = request.GET.get('messageID', None)

	message_to_delete = DirectMessage.objects.get(id=messageID)

	# Extra check to ensure the person deleting the message is the author
	if request.user == message_to_delete.author:

		# Delete the message
		message_to_delete.delete()

		return JsonResponse({"status": "success"})
	else:
		return JsonResponse({"status": "fail"})


@login_required
def save_image_form(request, dc_id):

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
			message = DirectMessage(
				directchat=DirectChat.objects.get(id=dc_id),
				author=request.user,
				date_sent = datetime.datetime.now(),
				content = data['content'],
				image = data['image']
			)


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

