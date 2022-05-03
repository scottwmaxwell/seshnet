# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


from django.contrib.auth.models import User
from .models import Message, Net
import datetime
from django.utils.html import urlize
from django.template.defaultfilters import linebreaksbr

import time

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.net_name = self.scope['url_route']['kwargs']['net_id']
        self.net_group_name = 'chat_%s' % self.net_name

        # Join net group
        await self.channel_layer.group_add(
            self.net_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave net group
        await self.channel_layer.group_discard(
            self.net_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):

        data = json.loads(text_data)
        
        user_id = data['user_id']
        message = data['message']
        
        # Urlize message for real-time chat
        message=urlize(message)

        if data['command'] == 'image':

            image_url = data['image_url']
            date_sent =data['date_sent']

            # Send message to net group
            await self.channel_layer.group_send(
                self.net_group_name,
                {
                    'type': 'image_message',
                    'message': message,
                    'user_id': user_id,
                    'image_url': image_url,
                    'date_sent': date_sent
                }
            )

        else:

            net_id = data['net_id']


            # Replace <div> and <br> in message with \n
            message=message.replace("<div>","")
            message=message.replace("</div>","")
            message=message.replace("<br>", "\n")

            # Save to database
            await self.save_message(net_id, user_id, message)

            # Put in <br> where \n exists for real-time chat
            message=linebreaksbr(message)

            # Send message to net group
            await self.channel_layer.group_send(
                self.net_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_id': user_id,
                }
            )

    # Receive message from net group
    async def chat_message(self, event):

        message = event['message']
        user_id = event['user_id']

        #Get username and profile pic url
        user_info = await self.get_user_info(user_id)

        username = user_info[0]
        user_image = user_info[1]

        # Get date...
        date_today = datetime.date.today()
        month = date_today.strftime("%B") 
        day =  date_today.strftime("%d") 
        year = date_today.today().strftime("%Y")  
        hour = str(datetime.datetime.now().hour) 
        minute = str(datetime.datetime.now().minute)
        time = datetime.datetime.strptime(f'{hour}:{minute}','%H:%M').strftime('%I:%M %p').replace('0','')
        date_sent = month + ' ' + day + ', ' + year + ', ' + str(time).lower()

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'date_sent': date_sent,
            'username': username,
            'user_image': user_image
        }))


    async def image_message(self, event):

        message = event['message']
        user_id = event['user_id']

        #Get username and profile pic url
        user_info = await self.get_user_info(user_id)

        username = user_info[0]
        user_image = user_info[1]

        image_url = event['image_url']
        date_sent = event['date_sent']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'date_sent': date_sent,
            'username': username,
            'user_image': user_image,
            'image_url': image_url
        }))


    @database_sync_to_async
    def get_user_info(self, user_id):
        user_id = int(user_id)
        username = User.objects.get(id=user_id).username
        image_url = User.objects.get(id=user_id).profile.image.url

        return (username, image_url)

    @database_sync_to_async
    def get_last_message(self, user_id):
        num = len(Message.objects.filter(author=User.objects.get(id=int(user_id))))
        num -= 1
        return Message.objects.filter(author=User.objects.get(id=int(user_id)))[num]

    @database_sync_to_async
    def save_message(self, net_id, user_id, message):

        return Message.objects.create(net= Net.objects.get(id=net_id),
                                      author = User.objects.get(id=user_id),
                                      date_sent = datetime.datetime.now(),
                                      content = message, 
                                      )



