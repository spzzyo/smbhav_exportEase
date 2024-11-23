from django.shortcuts import render
from django.http import JsonResponse
from .ml_model import predict  
from .forms import ImageUploadForm

def predict_view(request):
    result_label = None  # Initialize the result label
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
      
        if form.is_valid():
            uploaded_image = form.save()
          
            img_path = uploaded_image.item_image.path
            predictions = predict(img_path)
            class_names = ['bed', 'chair', 'sofa', 'swivelchair', 'table']
            
            max_index = predictions.argmax()
            result_label = class_names[max_index]

    else:
        form = ImageUploadForm()
        
  
    return render(request, 'mlModel/product.html', {'form': form, 'result_label': result_label})
