from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ChatmessageCreateForm
from .models import ChatGroup
# from .tasks import notify_customers


class Index(View):
    chat_group = get_object_or_404(ChatGroup, group_name="public")

    @method_decorator(login_required)
    def get(self, request):
        chat_messages = self.chat_group.chat_messages.prefetch_related(
            "author__profile").all()[:30]
        form = ChatmessageCreateForm()
        return render(request, 'chat/chat.html', {
            "PROJECT_TITLE": "Chat APP",
            "chat_messages": chat_messages,
            "form": form
            })

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

# def send_emails(request):
#     notify_customers.delay('Hello World!')
#     return redirect("home")
