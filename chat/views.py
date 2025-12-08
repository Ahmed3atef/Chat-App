from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ChatRoomEditForm, ChatmessageCreateForm, NewGroupForm
from .models import ChatGroup
from django.contrib import messages
# from .tasks import notify_customers


class ChatView(LoginRequiredMixin,View):
    def get(self, request, chatroom_name='public'):
        self.chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
        chat_messages = self.chat_group.chat_messages.prefetch_related( # type: ignore
            "author__profile")[:30]
        form = ChatmessageCreateForm()
        other_user = None
        if self.chat_group.is_private:
            if request.user not in self.chat_group.members.all():
                raise Http404
            for member in self.chat_group.members.all():
                if member != request.user:
                    other_user = member
                    break
        
        if self.chat_group.groupchat_name:
             if request.user not in self.chat_group.members.all():
                if request.user.emailaddress_set.filter(verified=True).exists():
                    self.chat_group.members.add(request.user)
                else:
                    messages.warning(request, 'You need to verify your email to join the chat!')
                    return redirect('profile-settings')
        context = {
            "PROJECT_TITLE": "Chat APP",
            "chat_messages": chat_messages,
            "form": form,
            "other_user": other_user,
            "chatroom_name": chatroom_name,
            "chat_group": self.chat_group,
        }
        return render(request, 'chat/chat.html', context)

    def post(self, request):
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = self.chat_group
            message.save()
            context = {
                "message": message,
                "user": request.user,
            }
            return render(request, 'chat/partials/chat_message_p.html', context)

class GetOrCreateChatroom(LoginRequiredMixin,View):
    
    def get(self, request, username):
        if request.user.username == username:
            return redirect('home')
        User = get_user_model()
        other_user = User.objects.get(username=username)
        my_chatrooms = request.user.chat_groups.filter(is_private=True)
        
        
        if my_chatrooms.exists():
            for chatroom in my_chatrooms:
                if other_user in chatroom.members.all():
                    chatroom = chatroom
                    break
                else:
                    chatroom = ChatGroup.objects.create(is_private=True)
                    chatroom.members.add(other_user, request.user)
        else:
            chatroom = ChatGroup.objects.create(is_private=True)
            chatroom.members.add(other_user, request.user)
        
        return redirect('chatroom', chatroom.group_name)
    
    
class CreateGroupChat(LoginRequiredMixin,View):
    def get(self,request):
        form = NewGroupForm()
        context = {
            'form':form
        }
        return render(request, 'chat/create_groupchat.html', context)
    
    def post(self, request):
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)
        else:
            context = {
                'form': form
            }
            return render(request, 'chat/create_groupchat.html', context)


class ChatroomEdit(LoginRequiredMixin, View):
    def get(self, request, chatroom_name):
        chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
        if request.user != chat_group.admin:
            raise Http404()
        form = ChatRoomEditForm(instance=chat_group)
        context = {
                'form': form,
                'chat_group': chat_group
            }
        return render(request, 'chat/chatroom_edit.html', context)
    
    def post(self, request, chatroom_name):
        chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        self.User = get_user_model()
        if form.is_valid():
            form.save()

            remove_members = request.POST.getlist('remove_members')
            
            for member_id in remove_members:
                member = self.User.objects.get(id=member_id)
                chat_group.members.remove(member)

            return redirect('chatroom', chatroom_name)
        
        
class ChatroomDelete(LoginRequiredMixin, View):
    def get(self, request, chatroom_name):
        chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
        if request.user != chat_group.admin:
            raise Http404()
        return render(request, 'chat/chatroom_delete.html', {'chat_group':chat_group})
    def post(self, request, chatroom_name):
        chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
        chat_group.delete()
        messages.success(request, 'Chatroom deleted')
        return redirect('home')
        

class ChatroomLeave(LoginRequiredMixin, View):
    def get(self, request, chatroom_name):
        chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
        if request.user not in chat_group.members.all():
            raise Http404()
        return render(request, 'chat/partials/modal_chat_leave.html')
    def post(self, request, chatroom_name):
        chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
        chat_group.members.remove(request.user)
        messages.success(request, 'You left the Chat')
        return redirect('home')




# def send_emails(request):
#     notify_customers.delay('Hello World!')
#     return redirect("home")
