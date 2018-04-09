"""
Model Trainer
"""

import numpy as np
import pandas as pd
import sqlite3
import pickle

n = 500

conn = sqlite3.connect("messages.db")
df = pd.read_sql("""select m1.messagetext as messagetext,
        ifnull(m2.is_sticker, 0) as gotsticker
        from messages m1 
        left join messages m2 
        on m1.messageid=m2.reply_messageid""", conn)

# clean and create bow
import cleaner
c = cleaner.Cleaner()
(dictionary, bows) = c.docs2bow(df["messagetext"], prune_at=n)

def bow2onehot(bow):
    vec = np.zeros(n, dtype=int)
    for word in bow:
        vec[word[0]] = word[1]
    return vec

vectors = [bow2onehot(x) for x in bows]

import keras
from keras.layers import Dense
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(np.asarray(vectors), df["gotsticker"].values, test_size=0.2, random_state=3)

np.random.seed(0)
nn = keras.models.Sequential()
nn.add(Dense(units=100, input_dim=n, activation='relu'))
nn.add(Dense(units=10, activation='relu'))
nn.add(Dense(units=1, activation='sigmoid'))
nn.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

nn_fit = nn.fit(X_train, Y_train, epochs=1000, verbose=0, 
        batch_size=len(X_train), initial_epoch=0)

print(nn.evaluate(X_test, Y_test, verbose=0))


nn.save("model.h5")
pickle.dump(dictionary, open("dictionary.p", "wb"))

print("entrenando el segundo modelo")

df = pd.read_sql("""select m1.messagetext as messagetext,
        ifnull(m2.is_sticker, 0) as gotsticker
        from messages m1 
        left join messages m2 
        on m1.messageid=m2.reply_messageid""", conn)


