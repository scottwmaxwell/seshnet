from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	profile_pic = models.ImageField(default='default.png', upload_to='profile_pics', blank=True)

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