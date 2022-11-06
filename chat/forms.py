from dataclasses import fields
from django import forms
from django.forms import ModelForm
from .models import ChatRoom, Profile
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = '__all__'
        exclude = ['host']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileForm(ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput,)
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']
