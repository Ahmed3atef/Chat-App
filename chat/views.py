from django.shortcuts import redirect, render
from django.views import View
# from .tasks import notify_customers

class Index(View):
    def get(self, request):
        return render(request, 'index.html', {"PROJECT_TITLE":"Chat APP"})
        


# def send_emails(request):
#     notify_customers.delay('Hello World!')
#     return redirect("home")