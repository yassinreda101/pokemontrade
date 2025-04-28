# chat/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .models import ChatRoom, ChatMessage
from .forms import RoomForm

@login_required
def room_list(request):
    # Get rooms the user is a participant in
    rooms = ChatRoom.objects.filter(participants=request.user).order_by('-created_at')
    return render(request, 'chat/room_list.html', {'rooms': rooms})

@login_required
def room(request, room_name):
    # Ensure room_name doesn't have any characters that would break the WebSocket URL
    safe_room_name = slugify(room_name)

    # Get or create the room
    room, created = ChatRoom.objects.get_or_create(name=safe_room_name)

    # Add user to participants if not already
    if request.user not in room.participants.all():
        room.participants.add(request.user)

    # Get messages for the room
    messages_list = ChatMessage.objects.filter(room=room).order_by('timestamp')

    return render(request, 'chat/room.html', {
        'room': room,
        'messages': messages_list
    })

@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, user=request.user)
        if form.is_valid():
            # Create the room
            room = form.save(commit=False)

            # Create a URL-friendly name
            room_name = slugify(room.name)
            room.name = room_name
            room.save()

            # Add participants
            room.participants.add(request.user)
            for participant in form.cleaned_data['participants']:
                room.participants.add(participant)

            messages.success(request, f"Chat room '{room.name}' created!")
            return redirect('chat:room', room_name=room.name)
    else:
        form = RoomForm(user=request.user)

    return render(request, 'chat/create_room.html', {'form': form})