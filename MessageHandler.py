import os

from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import pyrogram.enums

from message_repository import MessageRepository
from MongoDBConnection import MongoDBConnection

ADMIN_ID = os.getenv('ADMIN_ID')
ARSEN_ID = os.getenv('ARSEN_ID')
PIDOR_ID = os.getenv('PIDOR_ID')

db = MongoDBConnection()
message_repository = MessageRepository(db, 'messages')

async def handle_message(client: Client, message: Message):
    if message.text:
        message_repository.create_text_message(message.id, message.text, message.from_user.first_name, message.from_user.username, message.date)
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Отправить", callback_data=f"send_message_{message.id}")]])
        await client.send_message(chat_id=ARSEN_ID, text=message.text, reply_markup=keyboard)
        text = f"Name: {message.from_user.first_name}\nUsername: @{message.from_user.username}\nDate: {message.date}\nText: <code>{message.text}</code>"
        await client.send_message(chat_id=ADMIN_ID, text=text)
    if message.photo:
        message_repository.create_photo_message(message.id, message.photo.file_id, message.caption, message.from_user.first_name,
                                               message.from_user.username, message.date)
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Отправить", callback_data=f"send_message_{message.id}")]])
        await client.send_photo(chat_id=ARSEN_ID, photo=message.photo.file_id, caption=message.caption, reply_markup=keyboard)
        await client.send_photo(chat_id=ADMIN_ID, photo=message.photo.file_id, caption=message.caption)
    if message.voice:
        message_repository.create_voice_message(message.id, message.voice.file_id,
                                                message.from_user.first_name,
                                                message.from_user.username, message.date)
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Отправить", callback_data=f"send_message_{message.id}")]])
        await client.send_voice(chat_id=ARSEN_ID, voice=message.voice.file_id, reply_markup=keyboard)
        await client.send_voice(chat_id=ADMIN_ID, voice=message.voice.file_id)
    if message.video:
        message_repository.create_video_message(message.id, message.video.file_id,
                                                message.from_user.first_name,
                                                message.from_user.username, message.date)
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Отправить", callback_data=f"send_message_{message.id}")]])
        await client.send_video(chat_id=ARSEN_ID, video=message.video.file_id, reply_markup=keyboard)
        await client.send_video(chat_id=ADMIN_ID, video=message.video.file_id)
    if message.video_note:
        message_repository.create_video_note_message(message.id, message.video_note.file_id,
                                                message.from_user.first_name,
                                                message.from_user.username, message.date)
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Отправить", callback_data=f"send_message_{message.id}")]])
        await client.send_video_note(chat_id=ARSEN_ID, video_note=message.video_note.file_id, reply_markup=keyboard)
        await client.send_video_note(chat_id=ADMIN_ID, video_note=message.video_note.file_id)

async def handle_callback_query(client: Client, callback_query: CallbackQuery):
    message_id = int(callback_query.data.split("_")[-1])
    message = message_repository.get_message_by_id(message_id)
    from_user_name = message.get('from_user_name')
    from_user_username = message.get('from_user_username')
    date = message.get('date')
    message_type = message.get('type')
    if message_type == 'TEXT':
        text = f"Name: {from_user_name}\nUsername: @{from_user_username}\nDate: {date}\nText: <code>{message.get('text')}</code>"
        await client.send_message(chat_id=PIDOR_ID, text=text, parse_mode=pyrogram.enums.ParseMode.HTML)
        await client.send_message(chat_id=ARSEN_ID, text=text, parse_mode=pyrogram.enums.ParseMode.HTML)
    if message_type == 'PHOTO':
        caption = f"Name: {from_user_name}\nUsername: @{from_user_username}\nDate: {date}\nCaption: <code>{message.get('caption')}</code>"
        await client.send_photo(chat_id=PIDOR_ID, photo=message.get('file_id'), caption=caption, parse_mode=pyrogram.enums.ParseMode.HTML)
        await client.send_photo(chat_id=ARSEN_ID, photo=message.get('file_id'), caption=caption,
                                parse_mode=pyrogram.enums.ParseMode.HTML)
    if message_type == 'VOICE':
        caption = f"Name: {from_user_name}\nUsername: @{from_user_username}\nDate: {date}"
        await client.send_voice(chat_id=PIDOR_ID, voice=message.get('file_id'), caption=caption, parse_mode=pyrogram.enums.ParseMode.HTML)
        await client.send_voice(chat_id=ARSEN_ID, voice=message.get('file_id'), caption=caption,
                                parse_mode=pyrogram.enums.ParseMode.HTML)
    if message_type == 'VIDEO':
        caption = f"Name: {from_user_name}\nUsername: @{from_user_username}\nDate: {date}"
        await client.send_video(chat_id=PIDOR_ID, video=message.get('file_id'), caption=caption, parse_mode=pyrogram.enums.ParseMode.HTML)
        await client.send_video(chat_id=ARSEN_ID, video=message.get('file_id'), caption=caption,
                                parse_mode=pyrogram.enums.ParseMode.HTML)
    if message_type == 'VIDEO_NOTE':
        caption = f"Name: {from_user_name}\nUsername: @{from_user_username}\nDate: {date}"
        await client.send_video_note(chat_id=PIDOR_ID, video_note=message.get('file_id'))
        await client.send_video_note(chat_id=ARSEN_ID, video_note=message.get('file_id'))
        await client.send_message(chat_id=PIDOR_ID, text=caption, parse_mode=pyrogram.enums.ParseMode.HTML)
        await client.send_message(chat_id=ARSEN_ID, text=caption, parse_mode=pyrogram.enums.ParseMode.HTML)