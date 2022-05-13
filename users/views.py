from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignUpForm, ProfileUpdate, UpdateServerSettings, UpdateRole
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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

	if request.method == 'POST':
		user_id = request.POST.get('user')
		user = User.objects.get(id=user_id)

		form = UpdateRole(request.POST, instance=user.profile)
		if form.is_valid():
			form.save()



	if request.user.profile.role == "Admin":

		# Get all users
		users = User.objects.all()


		updateserversettings_form = UpdateServerSettings

		updaterole_forms = {}
		for user in users:

			updaterole_forms[user] = UpdateRole(initial={'role': user.profile.role })



		context = {
			'users':users,
			'updateserversettings_form': updateserversettings_form,
			'updaterole_forms': updaterole_forms,
		}

		return render(request, 'users/adminsettings.html', context)

	else:
		return render(request, 'users/error.html')
