from django.shortcuts import render

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

def upload_documents(request, category_id):
    if request.method == "POST":
        uploaded_files = request.FILES
        for file_key, file_obj in uploaded_files.items():
            # Save each file
            file_name = default_storage.save(f"documents/{file_obj.name}", file_obj)
            print(f"Saved: {file_name}")  # Debugging logs, optional

        return HttpResponse("Documents uploaded successfully!")
    else:
        return redirect(reverse('category:category-detail', args=[category_id]))

