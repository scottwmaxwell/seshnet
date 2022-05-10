from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignUpForm, ProfileUpdate
from django.contrib.auth.decorators import login_required

def signup(request):

	if request.method == 'POST':
		form = UserSignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'Account Created for {username}!')
			return redirect('login')

	else:
		form = UserSignUpForm()
	context = {"form":form}
	return render(request, 'users/signup.html', context)


@login_required
def settings(request):

	# Get user and pass it into template
	return render(request, 'users/settings.html')


@login_required
def profile(request):

	if request.method == 'POST':
		form = ProfileUpdate(request.POST, request.FILES, instance=request.user.profile)
		if form.is_valid():
			
			form.typing_indicator = form.cleaned_data.get('typing_indicator')
			form.online_indicator = form.cleaned_data.get('online_indicator')
			form.save()

	profile_update = ProfileUpdate

	context = {
		'profile_update': profile_update
	}

	return render(request, 'users/profile.html', context)


def adminsettings(request):

	if request.user.profile.role == "Admin":
		return render(request, 'users/adminsettings.html')

	else:
		return render(request, 'users/error.html')
