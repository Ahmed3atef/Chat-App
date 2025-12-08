from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('chat/<username>', views.GetOrCreateChatroom.as_view(), name="start-chat"),
    path('chat/room/<chatroom_name>', views.Index.as_view(), name="chatroom"),
    path('chat/new-groupchat/', views.CreateGroupChat.as_view(), name="new-groupchat")
    # path('send-emails/', views.send_emails, name='send_emails'),
]