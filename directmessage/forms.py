from django.forms import ModelForm, FileInput, TextInput
import django.forms as forms
from .models import DirectMessage

class UploadImageMessage(ModelForm):
	
	image = forms.ImageField(label='', required=False)
		
	class Meta:
		model = DirectMessage
		fields = ['content', 'image']

		widgets = {
			'content': TextInput(),
        	'image': FileInput()
        }