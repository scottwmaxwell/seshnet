from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	return render(request, 'directmessage/index.html')


@login_required
def directmessage(request, dm_id):
	return render(request, 'directmessage/directmessage.html')
