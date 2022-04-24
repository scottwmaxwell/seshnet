from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper

class UserSignUpForm(UserCreationForm):
	# email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper(self)

