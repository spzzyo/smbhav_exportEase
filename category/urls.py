from django.urls import path, include
from . import views

app_name = 'category'

urlpatterns = [
    path("", views.category_view, name="category")
]