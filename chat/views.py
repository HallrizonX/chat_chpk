import json

from django.shortcuts import render
from django.http import JsonResponse
from django.utils.safestring import mark_safe

from chat.models import Room, User


def index(request):
    users = User.objects.all().exclude(room__users=request.user)
    rooms = Room.objects.select_related().filter(users=request.user)
    counts = {}
    for room in rooms:
        count = room.message.filter(watched=False).exclude(user=request.user).count()
        count = room.message.filter(watched=False).exclude(user=request.user).count()
        counts[room.id] = count
    return render(request, 'index.html', {
        'users': users,
        'rooms': rooms,
        'counts': counts
    })


def create_room(request):
    return JsonResponse({'ok': True})


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
