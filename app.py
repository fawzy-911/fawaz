import os
import warnings
warnings.simplefilter("ignore")
#import tensorflow as tf
#from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
#import cv2


from flask import Flask, render_template, request
#, render_template_string, redirect, url_for, abort)
from werkzeug.utils import secure_filename
#from os import listdir

app = Flask(__name__)

#load the trained model
MODEL_PATH = "models/model_inception.h5"
model = load_model(MODEL_PATH)
#class_names = ['Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_healthy']
class_names = ['Bacterial_spot' ,'Early_blight', 'Late_blight' ,'Leaf_Mold' ,'Septoria_leaf_spot' ,'Spider_mites Two-spotted_spider_mite','Target_Spot','Tomato_Yellow_Leaf_Curl_Virus','Tomato_mosaic_virus','Healthy']
def model_predict(img_path, model):

    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    x=x/255
    x = np.expand_dims(x, axis=0)

    predictions = model.predict(x)
    label = class_names[np.argmax(predictions[0])]
    return label

@app.route('/', methods = ["GET"])
def index():
    return render_template('index.html')


@app.route('/predict',methods = ["GET", "POST"])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None        





if __name__ == "__main__":
    app.run(port=5001, debug=True)
