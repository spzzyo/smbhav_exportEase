from django.urls import path, include
from .views import chatPage
from .views import comparison, get_messages_and_summarize, make_protected_call, packreco, shiptrack, landing
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", landing, name= "landing"),
    path("carriers/", comparison, name="shipping-comparison" ),
    path("chat/", chatPage, name="chat-page"),
    path("summary/",get_messages_and_summarize, name='summarizemessages'),
    path('make-call/', make_protected_call, name='make_protected_call'),
    path("packaging/", packreco, name = "packing"),
    path("shiptrack/", shiptrack, name= "shiptrack")

]