from django.db import models
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User

class Net(models.Model):
	title = models.CharField(max_length=20, unique=True)


class Message(models.Model):
	net = models.ForeignKey(Net, on_delete = models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date_sent = models.DateTimeField(default=timezone.now, blank=True)
	content = models.TextField(null=True)
	image = models.ImageField(blank=True, upload_to='message_images')

	def save(self, *args, **kwargs):
		super(Message, self).save(*args, **kwargs)
		
		if self.image:
			img = Image.open(self.image.path)
			if img.height > 500 or img.width > 500:
				output_size = (500,500)
				img.thumbnail(output_size)
				img.save(self.image.path)

	def delete(self, *args, **kwargs):
		
		if self.image:
			storage, path = self.image.storage, self.image.path

		# Delete the model before the file
		super(Message, self).delete(*args, **kwargs)

		if self.image:
			# Delete the file after the model
			storage.delete(path)