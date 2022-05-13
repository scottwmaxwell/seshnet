from django.db import models
import uuid
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User

class DirectChat(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=20, unique=False)
	participants = models.ManyToManyField(User, related_name='participants', blank=True)

class DirectMessage(models.Model):
	directchat = models.ForeignKey(DirectChat, on_delete = models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date_sent = models.DateTimeField(default=timezone.now, blank=True)
	content = models.TextField(null=True)
	image = models.ImageField(blank=True, upload_to='message_images')

	def save(self, *args, **kwargs):
		super(DirectMessage, self).save(*args, **kwargs)
		
		if self.image:

			img = Image.open(self.image.path)
			if img.height > 500 or img.width > 500:
				output_size = (500,500)
				img.thumbnail(output_size)
				img.save(self.image.path)
