from django.contrib import admin

from .models import ChatRoom, Topic, Messages, Profile

admin.site.register(ChatRoom)
admin.site.register(Topic)
admin.site.register(Messages)
admin.site.register(Profile)
