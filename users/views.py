from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignUpForm, ProfileUpdate, UpdateServerSettings, UpdateRole
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ServerSettings

def signup(request):

	if request.method == 'POST':
		form = UserSignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'Account Created for {username}!')
			return redirect('login')


	if ServerSettings.objects.all():

		serversettings = ServerSettings.objects.all()[0]
		
		if serversettings.private == True:
			return render(request, 'users/error.html')


	form = UserSignUpForm()
	context = {"form":form, "serversettings":serversettings}

	return render(request, 'users/signup.html', context)


def signup_private(request, secret):

	if ServerSettings.objects.all():

		serversettings = ServerSettings.objects.all()[0]
		server_secret = serversettings.secret

		if secret == server_secret:

			if request.method == 'POST':
				form = UserSignUpForm(request.POST)
				if form.is_valid():
					form.save()
					username = form.cleaned_data.get('username')
					messages.success(request,f'Account Created for {username}!')
					return redirect('login')


			form = UserSignUpForm()
			context = {"form":form, "serversettings":serversettings}
			return render(request, 'users/signup.html', context)

	return render(request, 'users/error.html')



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

@login_required
def userRoles(request):

	if request.user.profile.role == "Admin":


		if request.method == 'POST':
			user_id = request.POST.get('user')
			user = User.objects.get(id=user_id)

			form = UpdateRole(request.POST, instance=user.profile)
			if form.is_valid():
				form.save()

		# Get all users
		users = User.objects.all()

		updaterole_forms = {}
		for user in users:

			updaterole_forms[user] = UpdateRole(initial={'role': user.profile.role })

		context = {
			'updaterole_forms': updaterole_forms,
		}

		return render(request, 'users/user_roles.html', context)

	else:
		return render(request, 'users/error.html')


@login_required
def serverSettings(request):

	if request.user.profile.role == "Admin":


		if request.method == 'POST':
			setting_id = request.POST.get('serversettings')
			serversetting = ServerSettings.objects.get(id=setting_id)

			form = UpdateServerSettings(request.POST, instance=serversetting)
			if form.is_valid():
				form.save()


		if ServerSettings.objects.all():
			# There should only ever be one of these
			serversetting = ServerSettings.objects.all()[0]

			updateserversettings = UpdateServerSettings(initial={
										'private':serversetting.private,
										'name':serversetting.name,
										'description': serversetting.description,
									})
		else:
			updateserversettings = UpdateServerSettings

			# Create serversetting since one does not exist

			serversetting = ServerSettings()
			serversetting.save()

		context ={
			'updateserversettings': updateserversettings,
			'serversetting_id': serversetting.id,
			'serversetting_secret': serversetting.secret
		}

		return render(request, 'users/server_settings.html', context)

	else:
		return render(request, 'users/error.html')

