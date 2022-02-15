from __future__ import print_function
import logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from comet_ml import Experiment

import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout


def main():
    
    mnist = tf.keras.datasets.mnist
    
    num_classes = 10

    # the data, shuffled and split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    

    x_train = x_train.reshape(60000, 784)
    x_test = x_test.reshape(10000, 784)
    x_train = x_train.astype("float32")
    x_test = x_test.astype("float32")
    x_train /= 255
    x_test /= 255
    print(x_train.shape[0], "train samples")
    print(x_test.shape[0], "test samples")

    # convert class vectors to binary class matrices
    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)


    train(x_train, y_train, x_test, y_test)

def build_model_graph(input_shape=(784,)):
    
    
    model = Sequential([
      Flatten(input_shape=(784, )),
      Dense(128, activation='relu'),
      Dense(128, activation='relu'),
      Dropout(0.2),
      Dense(10)
    ])

    loss_fn = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
    
    model.compile(optimizer='adam', 
                  loss=loss_fn,
                  metrics=['accuracy'])

    return model


def train(x_train, y_train, x_test, y_test):
    
    # Define model
    model = build_model_graph()

    model.fit(
        x_train,
        y_train,
        batch_size=120,
        epochs=25,
        validation_data=(x_test, y_test),
    )

    score = model.evaluate(x_test, y_test, verbose=0)
    logging.info("Score %s", score)
    
    model.save('my_model.h5')


if __name__ == "__main__":
    main()
