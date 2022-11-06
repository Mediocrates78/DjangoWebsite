from multiprocessing import context
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import ChatRoom, Topic, Messages, Profile
from .forms import RoomForm, UserForm, UserProfileForm

def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('chat')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('chat')
    context = {'page': page}
    return render(request, 'chat/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('chat')

def register_user(request):
    form = UserCreationForm()
    profileform = UserProfileForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profileform = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            
            Profile.objects.create(
                user = user,
                bio = request.POST.get('bio'),
                profile_pic = request.FILES.get('profile_pic')
            )

            login(request, user)
            return redirect('chat')

    return render(request, 'chat/login_register.html', {'form': form, 'profileform': profileform})

def chat(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    chatrooms = ChatRoom.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    rooms_count = chatrooms.count()
    chat_messages = Messages.objects.all().order_by('-created')

    context = {'chatrooms': chatrooms, 'topics': topics, 'rooms_count': rooms_count, 'chat_messages': chat_messages}
    return render(request, 'chat/chat.html', context)

def room(request, pk):
    room = ChatRoom.objects.get(id=pk)
    messages = room.messages_set.all().order_by('-created')

    if request.method == 'POST':
        message = Messages.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('room', pk=room.id)

    context = {'room': room, 'messages': messages}
    return render(request, 'chat/room.html', context)

def user_profile(request, pk):
    user = User.objects.get(id=pk)
    chatrooms = user.chatroom_set.all()
    chat_messages = user.messages_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'chatrooms': chatrooms, 'chat_messages': chat_messages, 'topics': topics}
    return render(request, 'chat/profile.html', context)

@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        ChatRoom.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('chat')

    context = {'form': form, 'topics': topics}
    return render(request, 'chat/chat_form.html', context)

@login_required(login_url='/login')
def update_room(request, pk):
    room = ChatRoom.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        messages.error(request, 'Only Room Hosts may edit a room.')
        return redirect('chat')
    else:
        if request.method == 'POST' and request.user == room.host:
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)
            room.name = request.POST.get('name')
            room.topic = topic
            room.decription = request.POST.get('decription')
            room.save()
            return redirect('chat')
        context = {'form': form, 'topics': topics, 'room': room}
        return render(request, 'chat/chat_form.html', context)

@login_required(login_url='/login')
def delete_room(request, pk):
    room = ChatRoom.objects.get(id=pk)
    if request.user != room.host:
        messages.error(request, 'Only Room Hosts may delete a room.')
        return redirect('chat')
    else:
        if request.method == 'POST' and request.user == room.host:
            room.delete()
            return redirect('chat')
        return render(request, 'chat/delete.html', {'obj': room})

@login_required(login_url='/login')
def delete_message(request, pk):
    message = Messages.objects.get(id=pk)
    if request.user != message.user:
        messages.error(request, 'Only the original poster may delete a message.')
        return redirect('chat')
    else:
        if request.method == 'POST' and request.user == message.user:
            message.delete()
            return redirect('chat')
        return render(request, 'chat/delete.html', {'obj': message})

@login_required(login_url='/login')
def update_user(request):
    user = request.user
    profile = user.profile
    form = UserForm(instance=user)
    profileform = UserProfileForm(instance=profile)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        profileform = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            profileform.save()
            
            return redirect('user_profile', pk=user.id)
    return render(request, 'chat/update_user.html', {'form': form, 'profileform': profileform})
    