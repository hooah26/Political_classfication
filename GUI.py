import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import pandas as pd
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt
import webbrowser
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5 import uic
from PyQt5.QtGui import *



form_window = uic.loadUiType('./app.ui')[0]


class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.path = None
        self.setupUi(self)
        self.model = load_model('.\output\community_classfication_model.h5')
        self.btn_check.clicked.connect(self.predict_C)
        self.btn_reset.clicked.connect(self.reset)
        self.btn_bbom.clicked.connect(self.btn_bbom1)
        self.btn_mlb.clicked.connect(self.btn_mlb1)
        self.btn_bobae.clicked.connect(self.btn_bobae1)


    def btn_bobae1(self):
        url = 'https://www.bobaedream.co.kr/'
        webbrowser.open(url)
    def btn_bbom1(self):
        url = 'https://www.ppomppu.co.kr/zboard/zboard.php?id=issue'
        webbrowser.open(url)
    def btn_mlb1(self):
        url = 'https://mlbpark.donga.com/mp/b.php?select=sct&m=search&b=bullpen&select=spf&query=%EC%A0%95%EC%B9%98'
        webbrowser.open(url)

    def reset(self):
        self.te_contents.clear()
        self.lbl_result.setText('다시 입력해주세요')

    def predict_C(self):
        content = self.te_contents.toPlainText()
        df = pd.DataFrame({'title': content}, index=[0])
        X = df.title
        # Y = 0

        with open('./output/encoder.pickle', 'rb') as f:
            encoder = pickle.load(f)
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
        # print(tokened_X)
        for i in range(len(tokened_X)):
            if len(tokened_X[i]) > 1778:
                tokened_X[i] = tokened_X[i][:1778]
        X_pad = pad_sequences(tokened_X, 1778)
        # print(X_pad)
        label = encoder.classes_
        model = load_model('C:\work\python\community\output\community_classfication_model.h5')

        preds = model.predict(X_pad)
        # print(preds)
        # print(label[np.argmax(preds)])

        predicts = []
        for pred in preds:
            predicts.append(label[np.argmax(pred)])
        df['predict'] = predicts

        if (df['predict'][0] == 'mlb'):
            output = '당신은  '+ '<font color=#ff0000>우회전</font>' +'을 선호합니다'

        else:
            output = '당신은  '+ '<font color=#0000ff>좌회전</font>'  +'을 선호합니다'


        self.lbl_result.setText(output)

app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())