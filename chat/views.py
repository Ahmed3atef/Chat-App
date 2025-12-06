from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from chat.models import ChatGroup
# from .tasks import notify_customers



class Index(View):
    @ method_decorator(login_required)
    def get(self, request):
        chat_group = get_object_or_404(ChatGroup, group_name="public")
        chat_messages= chat_group.chat_messages.prefetch_related("author__profile").all()[:30]
        return render(request, 'chat/chat.html', {"PROJECT_TITLE":"Chat APP", "chat_messages": chat_messages})
        


# def send_emails(request):
#     notify_customers.delay('Hello World!')
#     return redirect("home")