from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url="login-user")
def chatPage(request, *args, **kwargs):
    context = {}
    return render(request, "chat/chatPage.html", context)

@login_required(login_url="login-user")
def comparison(request, *args, **kwargs):
    context = {}
    return render(request, "home/tables.html", context)
