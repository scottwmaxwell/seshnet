from django.contrib import admin
from .models import Profile, ServerSettings

# Register your models here.
admin.site.register(Profile)
admin.site.register(ServerSettings)