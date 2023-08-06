import json
import asyncio
import time
import requests
from time import sleep
from threading import Thread
from .api import *
from pyshbullet.websocket._abnf import *
from pyshbullet.websocket._app import WebSocketApp
from pyshbullet.websocket._core import *
from pyshbullet.websocket._exceptions import *
from pyshbullet.websocket._logging import *
from pyshbullet.websocket._socket import *
unix_timestamp_to_datetime = lambda unix_timestamp : datetime.datetime.fromtimestamp(float(unix_timestamp), tzlocal.get_localzone())
class Receiver():
  def __init__(self, name, email, email_normalized, id):
    self.name = name
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
class User():
  def __init__(self, created, modified, email, email_normalized, id, image_url, max_upload_size, name):
    self.created = unix_timestamp_to_datetime(created)
    self.modified = unix_timestamp_to_datetime(modified)
    self.email = email
    self.email_normalized = email_normalized
    self.id = id
    self.image_url = image_url
    self.max_upload_size = max_upload_size
class Receiver():
  def __init__(self, email, email_normalized, id):
    self.email = email
    self.email_normalized = email_normalized
    self.id = id
class Listener():
  def __init__(self, apikey, events_list, user_obj):
    def on_message(ws, message):
      message_json = json.loads(message)
      if message_json['type'] == 'nop':
        pass
      if message_json['type'] == 'tickle':
        headers = {'Access-Token': apikey}
        resp = requests.get('https://api.pushbullet.com/v2/pushes?limit=1', headers=headers)
        resp_json = resp.json()
        if 'on_tickle' in events_list:
          loop = asyncio.new_event_loop()
          on_tickle = events_list['on_tickle']
          loop.run_until_complete(on_tickle(message_json['subtype']))
        if 'on_message' in events_list:
          on_message = events_list['on_message']
          loop = asyncio.new_event_loop()
          message = resp_json['pushes'][0]
          user = user_obj
          url = receiver = message_body = title = file_name = file_type = image_width = image_height = image_url = file_url = cursor = direction = None
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
          message_obj = Message(message['type'], title, message_body, message['created'], message['modified'], url, Sender(message['sender_name'], message['sender_email'], message['sender_email_normalized'], message['sender_iden']), Receiver(message['receiver_email'], message['receiver_email_normalized'], message['receiver_iden']), dismissed, file_name, file_type, image_width, image_height, image_url, file_url, cursor, direction)
          loop.run_until_complete(on_message(message_obj))
        else:
          pass
    ws = WebSocketApp(f'wss://stream.pushbullet.com/websocket/{apikey}', on_message=on_message)
    wst = Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()
    conn_timeout = 5
    while not ws.sock.connected and conn_timeout:
      sleep(1)
      conn_timeout -= 1
    msg_counter = 0
    while ws.sock.connected:
      ws.send(f'Heartbeat {msg_counter}')
      sleep(1)
      msg_counter += 1