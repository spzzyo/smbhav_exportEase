from django.urls import path, include
from .views import chatPage
from .views import comparison, get_messages_and_summarize
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("carriers/", comparison, name="shipping-comparison" ),
    path("chat/", chatPage, name="chat-page"),
    path("summary/",get_messages_and_summarize, name='summarizemessages'),

]