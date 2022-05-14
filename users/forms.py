from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from .models import Profile, ServerSettings

class UserSignUpForm(UserCreationForm):
	# email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper(self)


class ProfileUpdate(forms.ModelForm):

	class Meta:

		image = forms.ImageField(required=False)
		typing_indicator = forms.ChoiceField(choices=(True, False))
		online_indicator = forms.ChoiceField(choices=(True, False))

		model = Profile
		fields = ['image', 'typing_indicator', 'online_indicator']

		widgets = {
			'image':forms.FileInput()
		}

# Only for Admins
class UpdateRole(forms.ModelForm):

	class Meta:

		role = forms.ChoiceField(choices=('Admin', 'Moderator', 'User'))

		model = Profile
		fields = ['role']

class UpdateServerSettings(forms.ModelForm):

	class Meta:
		
		model = ServerSettings

		fields = ['name', 'description', 'private']

		widgets = {
			'private':forms.CheckboxInput(attrs={
                'data-toggle': 'toggle',
                'data-onstyle': 'default',
                'data-offstyle': 'default',
              	 })
		}

