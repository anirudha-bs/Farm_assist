import os
import requests
from flask import Flask, flash, request, redirect, url_for
from matplotlib import pyplot as plt
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import *


engine = create_engine("postgresql://postgres:abs%40aspire@localhost/testdb")
db = scoped_session(sessionmaker(bind=engine))
UPLOAD_FOLDER = '/home/anirudha/test_upload/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
name = None
min_temp=int()
max_temp=int()
weather_data= []

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])  
def upload():  
    return render_template('index.html') 
 
@app.route("/red")
def red():
    return render_template("upload_file.html")

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)
        global name
        name = UPLOAD_FOLDER + f.filename
        return redirect(url_for('predict'))  

@app.route('/predict', methods=['GET','POST'])
def predict():
    import tensorflow as tf
    import numpy as np
    from keras.preprocessing import image
    import h5py

    model = tf.keras.models.load_model('soil_classify.h5')
    
    global name
    image_path = name
    img = image.load_img(image_path, target_size=(128, 128))
    plt.imshow(img)
    img = np.expand_dims(img, axis=0)
    result = model.predict_classes(img)
    if result[0][0]:
        soil = "Red soil"
    else:
        soil = "Black soil"
    plt.title(soil)
    path='static/predicted.jpeg'
    plt.savefig(path)

    new_city=''
    if request.method == 'POST':
       new_city = str(request.form.get("city"))

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    r = requests.get(url.format('Bangalore')).json()
    global weather_data

    weather = {
        'city': new_city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    global min_temp
    global max_temp

    min_temp = int(5 / 9 * (r['main']['temp_min'] - 32))
    max_temp = int(5 / 9 * (r['main']['temp_max'] - 32))

    weather_data.append(weather)

    crop_types = db.execute("select crop from soildb where soil_type = :id1 and temp_min <= :id2 and temp_max >= :id3",{"id1": soil, "id2": min_temp, "id3": max_temp}).fetchall()


    return render_template('prediction.html',soil=soil,crop_types=crop_types,predicted_path = path,weather_data=weather_data)
  
if __name__ == '__main__':  
    app.run(debug = True)  
