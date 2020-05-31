import tensorflow as tf
import numpy as np
from keras.preprocessing import image
import h5py
from matplotlib import pyplot as plt
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

model = tf.keras.models.load_model('soil_classifier.h5')


image_path="red.jpg"
img = image.load_img(image_path, target_size=(128, 128))
plt.imshow(img)
img = np.expand_dims(img, axis=0)
result=model.predict_classes(img)

plt.title(result[0])
plt.show()


image_path1="black.jpg"
img1 = image.load_img(image_path1, target_size=(128, 128))
plt.imshow(img1)
img1 = np.expand_dims(img1, axis=0)
result=model.predict_classes(img1)

plt.title(result[0])
plt.show()


image_path1="all.jpg"
img1 = image.load_img(image_path1, target_size=(128, 128))
plt.imshow(img1)
img1 = np.expand_dims(img1, axis=0)
result=model.predict_classes(img1)

plt.title(result[0])
plt.show()


