from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from .models import Net, Message
from users import views
from django.contrib.auth.decorators import login_required
from .forms import UploadImageMessage
from django.http import JsonResponse
import datetime

def home(request):
	return render(request, 'nets/home.html')


@login_required
def index(request):

	nets = Net.objects.all()
	context = {
		'nets': nets,
	}
	return render(request, 'nets/index.html', context)


@login_required
def net(request, net_id):

	form = UploadImageMessage
	nets = Net.objects.all()
	messages = Message.objects.filter(net=Net.objects.get(id=net_id))
	context = {
		'net_id': net_id,
		'net_name': Net.objects.get(id=net_id).title,
		'messages': messages,
		'nets': nets,
		'form': form
	}
	return render(request, 'nets/net.html', context)



def save_image_form(request, net_id):

	if request.method == 'POST':
		form = UploadImageMessage(request.POST, request.FILES)
		if form.is_valid():

			# I might want to check if it's ajax request too...

			data = {"status": "valid", 
			        "content": form.cleaned_data["content"], 
			        "image": form.cleaned_data["image"]}

			print("\n\n\n\n")
			print(data["image"])
			print("\n\n\n")

			# Create a Message with the data...
			message = Message(net=Net.objects.get(id=net_id),
						      author=request.user,
						      date_sent = datetime.datetime.now(),
						      content = data['content'],
							  image = data['image'])


			# Let's save it to the database!
			message.save()

			# Let's return this data so that we can send it to the websocket!

			data = {
					"status":"valid",
				    "message":message.content,
				    "date_sent": message.date_sent,
				    "message":message.content,
				    "image_url":message.image.url,
				    "user": message.author.id
					}

		else:
			data={"status":"invalid"}


		return JsonResponse(data)
	