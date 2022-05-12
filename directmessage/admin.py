from django.contrib import admin

from .models import DirectChat, DirectMessage

# Register your models here.
admin.site.register(DirectChat)
admin.site.register(DirectMessage)
