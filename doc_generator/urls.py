from django.urls import path
from . import views

urlpatterns = [
    path('docBuddy/', views.doc_page, name='doc_page'),
    path('logistics/', views.logistics, name='logistics'),
]
