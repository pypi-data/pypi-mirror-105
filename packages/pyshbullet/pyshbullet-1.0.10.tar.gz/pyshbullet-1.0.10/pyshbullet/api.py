import aiohttp
import asyncio
import json
import datetime
import tzlocal
from threading import Thread
from time import sleep
from .listener import Listener
session = aiohttp.ClientSession()
unix_timestamp_to_datetime = lambda unix_timestamp : datetime.datetime.fromtimestamp(float(unix_timestamp), tzlocal.get_localzone())
class APIError(Exception):
  pass
class EventError(Exception):
  pass
class User():
  def __init__(self, created, modified, email, email_normalized, id, image_url, max_upload_size, name):
    self.created = unix_timestamp_to_datetime(created)
    self.modified = unix_timestamp_to_datetime(modified)
    self.email = email
    self.email_normalized = email_normalized
    self.id = id
    self.image_url = image_url
    self.max_upload_size = max_upload_size
    self.name = name
class Receiver():
  def __init__(self, email, email_normalized, id):
    self.email = email
    self.email_normalized = email_normalized
    self.id = id
class Sender():
  def __init__(self, name, email, email_normalized, id):
    self.name = name
    self.email = email
    self.email_normalized = email_normalized
    self.id = id
class Message():
  def __init__(self, type, title, content, sent, modified, message_url, author, reciever, dismissed, file_name, file_type, image_width, image_height, image_url, file_url, cursor, direction):
    self.type = type
    self.title = title
    self.content = content
    self.sent = unix_timestamp_to_datetime(sent)
    self.modified = unix_timestamp_to_datetime(modified)
    self.url = message_url
    self.author = author
    self.reciever = reciever
    self.dismissed = dismissed
    self.file_name = file_name
    self.file_type = file_type
    self.image_width = image_width
    self.image_height = image_height
    self.image_url = image_url
    self.file_url = file_url
    self.cursor = cursor
    self.direction = direction
class EventDecorator():
  def __init__(self):
    self.events = {}
  def __call__(self, func):
    if func.__name__ in self.events:
      raise EventError(f"The event function '{func.__name__}' has already been defined.")
    else:
      self.events[func.__name__] = func
    return None
class With():
  def __init__(self, type, email, email_normalized, id, image_url, name):
    self.type = type
    self.email = email
    self.email_normalized = email_normalized
    self.id = id
    self.image_url = image_url
    self.name = name
class Chat():
  def __init__(self, active, created, modified, id, chatting_with):
    self.active = active
    self.created = unix_timestamp_to_datetime(created)
    self.modified = unix_timestamp_to_datetime(modified)
    self.id = id
    self.chatting_with = chatting_with
class APIClient(): 
  def __init__(self, key):
    self.apikey = key
    self.event = EventDecorator()
  async def get_current_user(self):
    headers = {'Access-Token': self.apikey}
    async with session.get('https://api.pushbullet.com/v2/users/me', headers=headers) as resp:
      resp_json = await resp.json()
      try:
        return User(resp_json['created'], resp_json['modified'], resp_json['email'], resp_json['email_normalized'], resp_json['iden'], 'image_url', resp_json['max_upload_size'], resp_json['name'])
      except:
        raise APIError(f"{resp_json['error']['type']}: {resp_json['error']['message']}")
  async def get_push_history(self, modified_after = None, cursor = None, active = True, limit = None):
    headers = {'Access-Token': self.apikey}
    params = {'active': str(active).lower()}
    if modified_after is not None:
      params['modified_after'] = str(modified_after)
    if cursor is not None:
      params['cursor'] = str(cursor)
    if limit is not None:
      params['limit'] = str(limit)
    async with session.get('https://api.pushbullet.com/v2/pushes', headers=headers, params=params) as resp:
      resp_json = await resp.json()
      pushes = []
      user = await APIClient.get_current_user(self)
      url = receiver = message_body = title = file_name = file_type = image_width = image_height = image_url = file_url = cursor = direction = None
      for message in resp_json['pushes']:
        try:
          url = message['url']
        except:
          pass
        try:
          receiver = Receiver(message['receiver_email'], message['receiver_email_normalized'], message['receiver_iden'])
        except:
          pass
        try:
          message_body = message['body']
        except:
          pass
        try:
          title = message['title']
        except:
          pass
        try:
          file_name = message['file_name']
        except:
          pass
        try:
          file_type = message['file_type']
        except:
          pass
        try:
          image_width = message['image_width']
        except:
          pass
        try:
          image_height = message['image_height']
        except:
          pass
        try:
          image_url = message['image_url']
        except:
          pass
        try:
          file_url = message['file_url']
        except:
          pass
        try:
          cursor = message['cursor']
        except:
          pass
        try:
          direction = message['direction']
        except:
          pass
        dismissed = message['dismissed'] == 'true'
        pushes.append(Message(message['type'], title, message_body, message['created'], message['modified'], url, Sender(message['sender_name'], message['sender_email'], message['sender_email_normalized'], message['sender_iden']), Receiver(message['receiver_email'], message['receiver_email_normalized'], message['receiver_iden']), dismissed, file_name, file_type, image_width, image_height, image_url, file_url, cursor, direction))
      return pushes
  async def list_chats():
    pass
  def run(self):
    loop = asyncio.get_event_loop()
    if 'on_run' in self.event.events:
      on_run = self.event.events['on_run']
      loop.run_until_complete(on_run())
    Listener(self.apikey, self.event.events, loop.run_until_complete(APIClient.get_current_user(self)))