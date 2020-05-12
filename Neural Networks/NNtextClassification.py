# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:35:11 2020

@author: malyr
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

data = keras.datasets.imdb

num_words = 88000
(train_data, train_labels), (test_data , test_labels) = data.load_data(num_words = num_words)

word_index = keras.datasets.imdb.get_word_index()

word_index = {k:(v+3) for k,v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2  # unknown
word_index["<UNUSED>"] = 3

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

#trim data
train_data = keras.preprocessing.sequence.pad_sequences(train_data, value = word_index["<PAD>"], padding = "post", maxlen = 250)
test_data = keras.preprocessing.sequence.pad_sequences(test_data, value = word_index["<PAD>"], padding = "post", maxlen = 250)

def decode_review(text):
	return " ".join([reverse_word_index.get(i, "?") for i in text])



model = keras.Sequential()
model.add(keras.layers.Embedding(num_words,16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16,activation ="relu"))
model.add(keras.layers.Dense(1,activation = "sigmoid"))

model.summary()

model.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])

x_val = train_data[:10000]
x_train = train_data[:10000]

y_val = train_labels[:10000]
y_train = train_labels[:10000]



model.fit(train_data , train_labels , epochs = 40, batch_size = 512, validation_data = (x_val , y_val), verbose =1)

results = model.evaluate(test_data , test_labels)

print(results)

filename = "model.h5"
model.save(filename)
model = keras.models.load_model(filename)

def review_encode(s):
	encoded = [1]

	for word in s:
		if word.lower() in word_index:
			encoded.append(word_index[word.lower()])
		else:
			encoded.append(2)

	return encoded

with open("text.txt", encoding="utf-8") as f:
	for line in f.readlines():
		nline = line.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(":", "").replace("\"","").strip().split(" ")
		encode = review_encode(nline)
		encode = keras.preprocessing.sequence.pad_sequences([encode], value=word_index["<PAD>"], padding="post", maxlen=250) # make the data 250 words long
		predict = model.predict(encode)
		print(line)
		print(encode)
		print(predict[0])
        




i = 10
test_review = test_data[i]
predict = model.predict([test_review])
print(decode_review(test_review)) 
print("Prediction: " + str(predict[i]))
print("Actual: " + str(test_labels[i]))




# Source https://www.youtube.com/watch?v=Xmga_snTFBs&list=PLzMcBGfZo4-lak7tiFDec5_ZMItiIIfmj&index=8







