from django.forms import ModelForm, FileInput, TextInput
import django.forms as forms
from .models import DirectMessage, DirectChat

class UploadImageMessage(ModelForm):
	
	image = forms.ImageField(label='', required=False)
		
	class Meta:
		model = DirectMessage
		fields = ['content', 'image']

		widgets = {
			'content': TextInput(),
        	'image': FileInput()
        }


class CreateDirectChat(ModelForm):

	class Meta:
		model = DirectChat
		fields = ['participants']

		widgets = {
			'participants': TextInput()
		}