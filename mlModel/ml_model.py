import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import load_model
import numpy as np


model = load_model("C:/Users/YOSHITA/OneDrive/Desktop/smbhv/recentEXportEase/exportEase/mlModel/classification_model.h5")



def predict(image_path):
    
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)  
    img_array = np.expand_dims(img_array, axis=0)  
    img_array = preprocess_input(img_array) 
    
    predictions = model.predict(img_array)
    return predictions
