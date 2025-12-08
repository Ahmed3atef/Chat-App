from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ChatmessageCreateForm
from .models import ChatGroup
# from .tasks import notify_customers


class Index(View):
    
    @method_decorator(login_required)
    def get(self, request, chatroom_name='public'):
        self.chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
        chat_messages = self.chat_group.chat_messages.prefetch_related( # type: ignore
            "author__profile").all()[:30]
        form = ChatmessageCreateForm()
        other_user = None
        if self.chat_group.is_private:
            if request.user not in self.chat_group.members.all():
                raise Http404
            for member in self.chat_group.members.all():
                if member != request.user:
                    other_user = member
                    break
                
        context = {
            "PROJECT_TITLE": "Chat APP",
            "chat_messages": chat_messages,
            "form": form,
            "other_user": other_user,
            "chatroom_name": chatroom_name
        }
        return render(request, 'chat/chat.html', context)

    @method_decorator(login_required)
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

class GetOrCreateChatroom(View):
    
    @method_decorator(login_required)
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
    
    
    


# def send_emails(request):
#     notify_customers.delay('Hello World!')
#     return redirect("home")
