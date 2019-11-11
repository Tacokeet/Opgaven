import numpy as np
from os import walk
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
from random import randint
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Flatten, Conv2D
import re

def plotMatrix(data):
    plt.figure()
    plt.matshow(data)
    plt.show()


def plotImage(img, label):
    plt.imshow(img, cmap=matplotlib.cm.binary, interpolation='nearest')
    plt.axis('off')
    plt.title(label)
    plt.show()


def scaleData(X):
    return X / np.amax(X)


def buildModel():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(75, 75)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(40, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model


def confMatrix(labels, pred):
    # Retourneer de econfusion matrix op basis van de gegeven voorspelling (pred) en de actuele
    # waarden (labels). Check de documentatie van tf.math.confusion_matrix

    # YOUR CODE HERE
    return tf.math.confusion_matrix(
        labels,
        pred,
        num_classes=None,
        weights=None,
        dtype=tf.dtypes.int32,
        name=None
    )

# Laden van data #
f = []
labels = []
path = './Fundus-data/'
train_label = 0
train_labels = []
for (dirpath, dirnames, _) in walk(path):
    for dir in dirnames:
        for (_, _, filenames) in walk(path + dir):
            for file in filenames:
                f.append(path + dir + "/" + file)
                # pattern = '(\d*\.)'
                # result = re.findall(pattern, dir)
                # result = ''.join(result)
                # result = result[:-1]
                # print(result)
                if dir not in labels:
                    train_label += 1
                labels.append(dir)
                train_labels.append(train_label)
    break
# Prepareren van de data #
data = []
for file in f:
    img = Image.open(file).convert('L') # Open image and convert to grayscale
    imgdata = list(img.getdata())
    imgdata = np.reshape(imgdata, (75,75))
    data.append(imgdata)

data = np.array(data)
train_labels = np.array(train_labels)

# Het weergeven van een plaatje #
rnd = randint(0, data.shape[0])
plotImage(data[rnd], labels[rnd])

# Scale data #
data = scaleData(data)

# Aanmaken model en trainen van netwerk #
print ("")
print ("Aanmaken van het model.")
model = buildModel()
print ("Trainen van model..")
model.fit(data, train_labels, epochs=6)

print ("")
print ("Bepalen van de confusion matrix van het getrainde netwerk.")
pred = np.argmax(model.predict(data), axis=1)
cm = confMatrix(train_labels, pred)

print ("De confusion matrix:")
plotMatrix(cm)
