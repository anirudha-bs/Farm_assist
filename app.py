import os
import time
import requests
from flask import Flask, flash, request, redirect, url_for
from matplotlib import pyplot as plt
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import *

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

engine = create_engine(os.environ.get('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))
UPLOAD_FOLDER = 'uploaded_images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
name = None
min_temp=int()
max_temp=int()
city = ""


app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods = ['GET','POST'])
def upload():
    return render_template('index.html')

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js'), 200, {'Content-Type': 'text/javascript'}

@app.route('/manifest.json')
def manf():
    return app.send_static_file('manifest.json')

@app.route('/news', methods = ['GET'])
def news():
    return render_template('news.html')

@app.route('/schemes', methods = ['GET'])
def schemes():
    return render_template('schemes.html')

@app.route("/red")
def red():
    return render_template("upload_file.html")

@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        global city
        city=request.form.get("city")
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            filename = filename.split(".")
            filename = filename[0] + str(time.time()) + "." + filename[1]
            f.save(os.path.join(UPLOAD_FOLDER,filename))
            global name
            name = UPLOAD_FOLDER + filename
            return redirect(url_for('predict'))
        else:
            return "File format not supported"
    else:
        return "Get request not supported"

@app.route('/predict', methods=['GET','POST'])
def predict():
    import tensorflow as tf
    import numpy as np
    from keras.preprocessing import image
    import h5py

    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    model = tf.keras.models.load_model('soil_classifier.h5')

    global name
    image_path = name
    img = image.load_img(image_path, target_size=(128, 128))
    plt.imshow(img)
    img = np.expand_dims(img, axis=0)
    result = model.predict_classes(img)
    if result[0]== 2:
        soil = "Red soil"
    elif result[0]== 1:
        soil = "Black soil"
    else:
        soil="Alluvial soil"
    plt.title(soil)
    path='static/predicted_images/' + "predicted" + str(time.time()) + ".jpeg"
    plt.savefig(path)

    global city

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    r = requests.get(url.format(city)).json()
    global weather_data

    weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    global min_temp
    global max_temp

    min_temp = int(5 / 9 * (r['main']['temp_min'] - 32))
    max_temp = int(5 / 9 * (r['main']['temp_max'] - 32))


    crop_types = db.execute("select crop,temp_min,temp_max,rainfall from soildb where soil_type = :id1 and temp_min <= :id2 and temp_max >= :id3",{"id1": soil, "id2": min_temp, "id3": max_temp}).fetchall()


    return render_template('prediction.html',soil=soil,crop_types=crop_types,predicted_path = path,weather_data=weather,city=city)

if __name__ == '__main__':
    app.run(debug = True)
