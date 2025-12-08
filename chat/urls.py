from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatView.as_view(), name='home'),
    path('chat/<username>', views.GetOrCreateChatroom.as_view(), name="start-chat"),
    path('chat/room/<chatroom_name>', views.ChatView.as_view(), name="chatroom"),
    path('chat/new-groupchat/', views.CreateGroupChat.as_view(), name="new-groupchat"),
    path('chat/edit/<chatroom_name>', views.ChatroomEdit.as_view(), name="edit-chatroom"),
    path('chat/delete/<chatroom_name>', views.ChatroomDelete.as_view(), name="chatroom-delete"),
    path('chat/leave/<chatroom_name>', views.ChatroomLeave.as_view(), name="chatroom-leave"),
    path('chat/fileupload/<chatroom_name>', views.ChatFileUpload.as_view(), name="chat-file-upload"),
    # path('send-emails/', views.send_emails, name='send_emails'),
]