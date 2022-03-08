from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignUpForm


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