from django.shortcuts import render
from doc_manager.models import Document
from doc_manager.enc_utils import handle_document_upload

# Create your views here.
def category_view(request):
    return render(request, "Category/category_view.html")

# category/views.py
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.urls import reverse

def category_detail(request, category_id):
    categories = {
        1: "Fruits",
        2: "Furniture",
        3: "Electronics",
        4: "Clothes",
    }
    category_name = categories.get(category_id, "Unknown Category")

    # List of required documents for this category
    required_documents = [
        "Business Registration Certificate",
        "Tax Identification Number (TIN)",
        # "Proof of Address",
        # "Bank Account Statement",
    ]

    context = {
        'category_id': category_id,
        'category_name': category_name,
        'required_documents': required_documents,
    }
    return render(request, 'category/category_detail.html', context)

# def upload_documents(request, category_id):
#     categories = {
#         1: "Fruits",
#         2: "Furniture",
#         3: "Electronics",
#         4: "Clothes",
#     }

#     # Check if the category exists
#     if category_id not in categories:
#         return HttpResponse("Category not found", status=404)
    
#     category_name = categories[category_id]

#     if request.method == 'POST':
#         # Get the documents from the form
#         required_documents = request.FILES.getlist('document_1')  # Example for one document, you can loop through all
#         additional_document = request.FILES.get('additional_documents')

#         # Create a new Document entry
#         for document in required_documents:
#             doc = Document(exporter=request.user, title=document.name, original_file=document)
#             doc.save()
#             handle_document_upload(doc.original_file.path, request.user.id, category_name)  # Call the document upload function (watermark, encrypt, upload to S3)

#         if additional_document:
#             doc = Document(exporter=request.user, title=additional_document.name, original_file=additional_document)
#             doc.save()
#             handle_document_upload(doc.original_file.path, request.user.id, category_name)

#         return HttpResponse("Documents uploaded and encrypted successfully")

#     # For GET request, show the form to upload documents
#     required_documents = ["Document 1", "Document 2", "Document 3"]  # Hardcoded list for now
#     return render(request, "category/upload_documents.html", {
#         "category_name": category_name,
#         "category_id": category_id,
#         "required_documents": required_documents,
#     })
def upload_documents(request, category_id):
    categories = {
        1: "Fruits",
        2: "Furniture",
        3: "Electronics",
        4: "Clothes",
    }

    # Check if the category exists
    if category_id not in categories:
        return HttpResponse("Category not found", status=404)
    
    category_name = categories[category_id]

    if request.method == 'POST':
        # Get the documents from the form
        required_documents = request.FILES.getlist('document_1')  # Example for one document, you can loop through all
        additional_document = request.FILES.get('additional_documents')

        # Handle required documents (including PDFs)
        for document in required_documents:
            if document.name.endswith('.pdf') or document.name.endswith(('.jpg', '.png', '.docx', '.doc')):
                doc = Document(exporter=request.user, title=document.name, original_file=document)
                doc.save()
                handle_document_upload(doc.original_file.path, request.user.id, category_name, doc)

        # Handle additional document (if uploaded)
        if additional_document:
            if additional_document.name.endswith('.pdf') or additional_document.name.endswith(('.jpg', '.png', '.docx', '.doc')):
                doc = Document(exporter=request.user, title=additional_document.name, original_file=additional_document)
                doc.save()
                handle_document_upload(doc.original_file.path, request.user.id, category_name, doc)

        return HttpResponse("Documents uploaded and encrypted successfully")

    # For GET request, show the form to upload documents
    required_documents = ["Document 1", "Document 2", "Document 3"]  # Hardcoded list for now
    return render(request, "category/upload_documents.html", {
        "category_name": category_name,
        "category_id": category_id,
        "required_documents": required_documents,
    })