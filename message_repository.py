from datetime import datetime

from pymongo.errors import DuplicateKeyError
from typing import Optional, Dict, Any

from MongoDBConnection import MongoDBConnection

class MessageRepository:
    def __init__(self, db_connection: MongoDBConnection, collection_name: str = 'messages'):
        self.collection = db_connection.db[collection_name]

    def create_text_message(self, message_id: int, text: str, from_user_name: str, from_user_username: str, date: datetime) -> Optional[Dict[str, Any]]:
        message_data = {
            '_id': message_id,
            'type': 'TEXT',
            'text': text,
            'from_user_name': from_user_name,
            'from_user_username': from_user_username,
            'date': date
        }

        try:
            result = self.collection.insert_one(message_data)
            if result.inserted_id:
                return self.get_message_by_id(message_id)
            return None
        except DuplicateKeyError:
            return None

    def create_photo_message(self, message_id: int, file_id: str, caption: str, from_user_name: str, from_user_username: str, date: datetime) -> Optional[Dict[str, Any]]:
        message_data = {
            '_id': message_id,
            'type': 'PHOTO',
            'file_id': file_id,
            'caption': caption,
            'from_user_name': from_user_name,
            'from_user_username': from_user_username,
            'date': date
        }

        try:
            result = self.collection.insert_one(message_data)
            if result.inserted_id:
                return self.get_message_by_id(message_id)
            return None
        except DuplicateKeyError:
            return None

    def create_voice_message(self, message_id: int, file_id: str, from_user_name: str, from_user_username: str, date: datetime) -> Optional[Dict[str, Any]]:
        message_data = {
            '_id': message_id,
            'type': 'VOICE',
            'file_id': file_id,
            'from_user_name': from_user_name,
            'from_user_username': from_user_username,
            'date': date
        }

        try:
            result = self.collection.insert_one(message_data)
            if result.inserted_id:
                return self.get_message_by_id(message_id)
            return None
        except DuplicateKeyError:
            return None

    def create_video_message(self, message_id: int, file_id: str, from_user_name: str, from_user_username: str, date: datetime) -> Optional[Dict[str, Any]]:
        message_data = {
            '_id': message_id,
            'type': 'VIDEO',
            'file_id': file_id,
            'from_user_name': from_user_name,
            'from_user_username': from_user_username,
            'date': date
        }

        try:
            result = self.collection.insert_one(message_data)
            if result.inserted_id:
                return self.get_message_by_id(message_id)
            return None
        except DuplicateKeyError:
            return None

    def create_video_note_message(self, message_id: int, file_id: str, from_user_name: str, from_user_username: str, date: datetime) -> Optional[Dict[str, Any]]:
        message_data = {
            '_id': message_id,
            'type': 'VIDEO_NOTE',
            'file_id': file_id,
            'from_user_name': from_user_name,
            'from_user_username': from_user_username,
            'date': date
        }

        try:
            result = self.collection.insert_one(message_data)
            if result.inserted_id:
                return self.get_message_by_id(message_id)
            return None
        except DuplicateKeyError:
            return None

    def get_message_by_id(self, message_id: int) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({'_id': message_id})