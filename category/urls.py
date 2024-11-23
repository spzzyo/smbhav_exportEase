from django.urls import path, include
from . import views

app_name = 'category'

urlpatterns = [
    path("category/", views.category_view, name="category"),
    path('<int:category_id>/', views.category_detail, name='category-detail'),
    path("<int:category_id>/upload-documents/", views.upload_documents, name="upload-documents"),
]