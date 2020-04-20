from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
from keras import regularizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
from keras.preprocessing import image
import os
import numpy as np
import matplotlib.pyplot as plt

# defining classes

def soil(result):
    soil_type=""
    if result[0]==2:
       soil_type="Red soil"
    elif result[0]==1:
       soil_type="Black soil"
    else:
       soil_type="Alluvial soil"
    return soil_type


# Adding dataset paths

PATH = 'new_datasets'

train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')
test_dir = os.path.join(PATH, 'test')

train_red_dir = os.path.join(train_dir, 'Red_soil')
validation_red_dir = os.path.join(validation_dir, 'Red_soil')

train_black_dir = os.path.join(train_dir, 'Black_soil')
validation_black_dir = os.path.join(validation_dir, 'Black_soil')

train_all_dir = os.path.join(train_dir, 'Alluvial_soil')
validation_all_dir = os.path.join(validation_dir, 'Alluvial_soil')

num_soil_tr = len(os.listdir(train_red_dir)) + len(os.listdir(train_black_dir)) +len(os.listdir(train_all_dir))
num_soil_val = len(os.listdir(validation_red_dir)) + len(os.listdir(validation_black_dir)) + len((os.listdir(validation_all_dir)))

print("Total training images = ",num_soil_tr)
print("Total validation images = ",num_soil_val)

# hyperparameters

batch_size = 100
epochs = 15
IMG_HEIGHT = 128
IMG_WIDTH = 128
classes_num=3

# data generators

train_image_generator = ImageDataGenerator(rescale=1./255)

validation_image_generator = ImageDataGenerator(rescale=1./255)

train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='categorical')

val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=validation_dir,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           shuffle=True,
                                                           class_mode='categorical')

# defining the model

model = Sequential([
    Conv2D(16, 5, activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
    MaxPooling2D(pool_size=(3, 3)),
    Dropout(0.2),
    Conv2D(32, 5, activation='relu'),
    MaxPooling2D(pool_size=(3, 3)),
    Dropout(0.2),
    Conv2D(64, 5, activation='relu'),
    MaxPooling2D(pool_size=(3, 3)),
    Dropout(0.3),
    Flatten(),
    Dense(32, activation='relu'),
    Dense(classes_num, activation='softmax')
])


model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

model.summary()

history = model.fit_generator(
    train_data_gen,
    steps_per_epoch= num_soil_tr// batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=num_soil_val // batch_size
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

# training and validation graphs

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()


model.save('new_soil_classify.h5')


# for testing trained model with images differnent class

image_path="red.jpg"
img = image.load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
plt.imshow(img)
img = np.expand_dims(img, axis=0)
result=model.predict_classes(img)
plt.title(result[0])
plt.show()


image_path1="black.jpg"
img1 = image.load_img(image_path1, target_size=(IMG_HEIGHT, IMG_WIDTH))
plt.imshow(img1)
img1 = np.expand_dims(img1, axis=0)
result=model.predict_classes(img1)
plt.title(result[0])
plt.show()

image_path="all.jpg"
img = image.load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
plt.imshow(img)
img = np.expand_dims(img, axis=0)
result=model.predict_classes(img)
plt.title(result[0])
plt.show()

