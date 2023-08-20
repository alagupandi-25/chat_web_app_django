import json
from main.models import Chat,CustomUser
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        user_id = self.scope['user'].id
        receiver_id=self.scope['url_route']['kwargs']['other_user_id']
      
        if int(user_id) > int(receiver_id):
            self.room_name = f'{user_id}-{receiver_id}'
        else:
            self.room_name = f'{receiver_id}-{user_id}'
        
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        
        data = json.loads(text_data)
        message = data.get("message")
        sender_id=data.get("sender_id")
        receiver_id=data.get("receiver_id")
        
        await self.save_message(sender_id,receiver_id, self.room_name, message)

        await self.channel_layer.group_send(
            self.room_name, {
                'type': 'chat_message',
                'sender_id':sender_id,
                'receiver_id':receiver_id,
                'message': message,
                
            }
        )

    async def chat_message(self, event):
        
        message = event.get('message', '')
        sender_id = event.get('sender_id', '')
        receiver_id = event.get('receiver_id', '')
        
        await self.send(text_data=json.dumps(
            {
                'type': 'chat_message',
                'sender_id':sender_id,
                'receiver_id':receiver_id,
                'message': message,
            }
        ))
        
    @database_sync_to_async
    def save_message(self, sender_id,receiver_id, thread_name, message):
        
        sender = CustomUser.objects.get(id=sender_id)
        receiver = CustomUser.objects.get(id=receiver_id)

        message = Chat.objects.create(sender=sender,receiver=receiver,message=message,thread_name=thread_name)
        message.save()
        
    


        
