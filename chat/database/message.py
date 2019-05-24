from chat.models import Room
import re


async def messages_response(messages: Room) -> str:
    old_messages: str = ""

    for msg in messages:
        if msg.user:
            old_messages += f"{msg.user}: {msg.text} \n"
        else:
            old_messages += f"Anon: {msg.text} \n"

    old_messages += "<< Історія"

    return old_messages


async def format_message(username: str, message: str) -> str:
    return f"{username}: {message}"


async def valid_message(message: str) -> bool:
    if re.findall("^\s*$", message):
        return False
    return True
