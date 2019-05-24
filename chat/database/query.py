from chat.models import Room, Message, User
from channels.db import database_sync_to_async


@database_sync_to_async
def create_new_room(room_name: str):
    new = False
    try:
        Room.objects.get(slug=room_name)
    except:
        try:
            Room.objects.get(slug="_".join(reversed(room_name.split('_'))))
        except:
            new = Room.objects.create(slug=room_name)

    if new:
        users = room_name.split('_')
        relations = [User.objects.get(username=name) for name in users]
        room = Room.objects.get(slug=new.slug)
        room.title = room_name
        for user in relations:
            room.users.add(user)
        room.save()
        return True

    return False


@database_sync_to_async
def get_old_messages(username: str,room_name: str):
    try:
        room = Room.objects.select_related().get(slug=room_name)
        messages = room.message.all().order_by('id')
        user = User.objects.get(username=username)
        for message in messages.filter(watched=False).exclude(user=username):
            message.watched = True
            message.save()
        return [room, messages]
    except Room.DoesNotExist:
        return [False, False]


@database_sync_to_async
def write_message_to_db(room_name: str, username: str, msg: str):
    try:
        msg = Message.objects.create(user=username, text=msg)
        room = Room.objects.get(slug=room_name)
        room.message.add(msg)
    except Exception:
        return False

    return True
