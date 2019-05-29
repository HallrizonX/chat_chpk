from chat.models import Room
import re


async def messages_response(messages: Room) -> str:
    old_messages: str = ""

    for msg in messages:
        if msg.user:
            old_messages += f"<p class='message'> <span class='username'>{msg.user}</span>: {msg.text} </p>"
        else:
            old_messages += f"Anon: {msg.text} \n"

    return old_messages


async def format_message(username: str, message: str) -> str:
    return f"<p class='message'> <span class='username'>{username}</span>: {message} </p>"


async def valid_message(message: str) -> bool:
    if re.findall("^\s*$", message):
        return False
    return True
