from django.urls import path, include
from .views import request_document_access

urlpatterns = [
    path("request-document/<int:document_id>/", request_document_access, name="request_document_access"),
]