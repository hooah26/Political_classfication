import sys
# from PyQt5.QtWidgets import *
# from PyQt5 import uic
# from PyQt5.QtCore import QCoreApplication
# from PyQt5.QtGui import QPixmap
# from PIL import Image
import numpy as np
import pandas as pd
import pickle
from konlpy.tag import Okt
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())
exit()

content = '윤석열은 똑똑해 내생각엔 이번엔 윤석열이 잘할것같음'

df = pd.DataFrame({'title': content}, index=[0])
X = df.title
# Y = 0

with open('./output/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
#
# labeled_Y = encoder.transform(Y)
# print(encoder.classes_)
# print(labeled_Y[:5])

# onehot_Y = to_categorical(labeled_Y)
# print(onehot_Y)

okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)

stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)
# print(X[:10])

with open('output/token.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_X = token.texts_to_sequences(X)

for i in range(len(tokened_X)):
    if len(tokened_X[i]) > 1785:
        tokened_X[i] = tokened_X[i][:1785]
X_pad = pad_sequences(tokened_X, 1785)

label = encoder.classes_
model = load_model('./community_classfication_model.h5')

preds = model.predict(X_pad)
# print(X_pad)

predicts = []
for pred in preds:
    predicts.append(label[np.argmax(pred)])
df['predict'] = predicts

if (df['predict'][0] == 'bobae'):
    output = '당신은 파란 성향입니다'
else:
    output = '당신은 빨간 성향입니다.'


print(output)

