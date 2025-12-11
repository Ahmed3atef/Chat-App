# [file name]: consumers.py
from chat.models import ChatGroup, GroupMessage
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from channels.generic.websocket import WebsocketConsumer
import json



class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(
            ChatGroup, group_name=self.chatroom_name)

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )

        # add and update online users
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )

        # remove and update online users
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
            'chat_group': self.chatroom,
        }
        html = render_to_string(
            "chat/partials/chat_message_p.html", context=context)

        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1

        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def online_count_handler(self, event):
        online_count = event['online_count']
        User = get_user_model()

        chat_messages = ChatGroup.objects.get(
            group_name=self.chatroom_name).chat_messages.all()[:30]
        author_ids = set([message.author.id for message in chat_messages])
        users = User.objects.filter(id__in=author_ids)

        context = {
            'online_count': online_count,
            'chat_group': self.chatroom,
            'users': users
        }
        html = render_to_string("chat/partials/online_count.html", context)
        self.send(text_data=html)


class OnlineStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.group_name = 'online-status'

        # Instead of trying to get a ChatGroup, we'll use a simple dictionary
        # or create a separate model for tracking online status if needed
        # For now, we'll just use the channel layer without a ChatGroup
        self.channel_group_name = 'global-online-status'

        async_to_sync(self.channel_layer.group_add)(
            self.channel_group_name, self.channel_name
        )

        self.accept()
        self.update_online_status()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_group_name, self.channel_name
        )
        self.update_online_status()

    def receive(self, text_data):
        # This consumer doesn't need to receive messages
        pass


    def update_online_status(self):
        # Get all chat groups where the user is a member
        User = get_user_model()

        # Get online users from all chat groups
        all_online_users = set()
        for chat_group in ChatGroup.objects.all():
            all_online_users.update(chat_group.users_online.all())

        online_users = User.objects.filter(
            id__in=[user.id for user in all_online_users])

        # Get the user's chat groups
        my_chats = self.user.chat_groups.all()

        # Check which chats have other users online
        public_chat = ChatGroup.objects.filter(group_name='public').first()
        public_chat_users = []
        if public_chat:
            public_chat_users = public_chat.users_online.exclude(
                id=self.user.id)

        private_chats_with_users = []
        group_chats_with_users = []

        for chat in my_chats:
            online_in_chat = chat.users_online.exclude(id=self.user.id)
            if online_in_chat.exists():
                if chat.is_private:
                    private_chats_with_users.append(chat)
                elif chat.groupchat_name:
                    group_chats_with_users.append(chat)

        online_in_chats = bool(
            public_chat_users or private_chats_with_users or group_chats_with_users)

        context = {
            'online_users': online_users.exclude(id=self.user.id),
            'online_in_chats': online_in_chats,
            'public_chat_users': public_chat_users,
            'user': self.user
        }

        html = render_to_string(
            "chat/partials/online_status.html", context=context)

        # Send to all connected clients
        async_to_sync(self.channel_layer.group_send)(
            self.channel_group_name,
            {
                'type': 'send_online_status',
                'html': html
            }
        )

    def send_online_status(self, event):
        # Send the rendered HTML to the client
        self.send(text_data=event['html'])


