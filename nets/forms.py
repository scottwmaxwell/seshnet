from django.forms import ModelForm, FileInput, TextInput
import django.forms as forms
from .models import Message, Net

class UploadImageMessage(ModelForm):
	
	image = forms.ImageField(label='', required=False)
		
	class Meta:
		model = Message
		fields = ['content', 'image']

		widgets = {
			'content': TextInput(),
        	'image': FileInput()
        }

class CreateNet(ModelForm):

	class Meta:
		model = Net
		fields = ['title']

		widgets = {
			'title': TextInput()
		}