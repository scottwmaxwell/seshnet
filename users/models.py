from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
	
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)
	typing_indicator = models.BooleanField(default=True)

	ADMIN = 'Admin'
	MODERATOR = 'Moderator'
	USER = 'User'
    
	ROLE_CHOICES = [
		(ADMIN, 'Admin'),
		(MODERATOR, 'Moderator'),
		(USER, 'User'),

	]

	role = models.CharField(
		max_length=20,
		choices=ROLE_CHOICES,
		default=USER,
	)


	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)
		
		if self.image:

			img = Image.open(self.image.path)
			if img.height > 500 or img.width > 500:
				output_size = (500,500)
				img.thumbnail(output_size)
				img.save(self.image.path)