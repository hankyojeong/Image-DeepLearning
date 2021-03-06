from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import numpy as np
import os

categories = ["chair", "camera", "butterfly", "elephant", "flamingo"]
nb_classes = len(categories)

#Set the image size
image_w = 64
image_h = 64

#Open the Data
X_train, X_test, y_train, y_test = np.load("./image/5obj.npy")
#Regulate the Data
X_train = X_train.astype("float") / 256
X_test = X_test.astype("float") / 256
print('X_train shape:', X_train.shape)

#Construct the Model
model = Sequential()
model.add(Convolution2D(32,3,3,border_mode='same',input_shape=X_train.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Convolution2D(64, 3, 3, border_mode='same'))
model.add(Activation('relu'))

model.add(Convolution2D(64, 3, 3))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

#Train the model
#Save the Model using h5py
hdf5_file = "./image/5obj-model.hdf5"
if os.path.exists(hdf5_file):
    #Load the already trained model 
    model.load_weights(hdf5_file)
else:
    model.fit(X_train, y_train, batch_size=32, nb_epoch=50)
    #Save the trained model
    model.save_weights(hdf5_file)


#Estimate the model
score = model.evaluate(X_test, y_test)
print('loss=',score[0])
print('accuracy=',score[1])