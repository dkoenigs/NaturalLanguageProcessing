#Importing webpage retreival library
import urllib3
#Importing a HTML parsing library
from bs4 import BeautifulSoup
#Importing text editing libraries
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
#Importing Frequency list
from nltk.probability import FreqDist
#Importing Heap queue
from heapq import nlargest
#Importing Dictionary data structure to store (keys = sentences, values = significance score based on number of significant words contained)
from collections import defaultdict
#Import PyQt5
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5 import QtCore, QtWidgets
import sys
from PyQt5.Qt import QInputDialog, QPlainTextEdit


class SummarizeText():
    summarizedText = ""
    articlText = ""
    n = 0
    def __init__(self, articleText, n):
        self.articlText = articleText
        self.n = n

    # def getUrlText(self, articleUrl):
    #     http = urllib3.PoolManager()
    #     response = http.request('GET', articleUrl)
    #     soup = BeautifulSoup(response.data, features="html.parser")
    #     textOnly = soup.find(class_= 'entry-content').text
    #     return textOnly

    def getNonStopwords(self, words):
        stopWords = set(stopwords.words('english') + list(punctuation))
        nonStopWords = []
        for word in words:
            if word not in stopWords:
                nonStopWords.append(word)
        return nonStopWords

    def getSentenceRankings(self, sentences, freq):
        #For each sentence (i) go through all words in the sentence and look up how often it
        #occurs in the text overall (freq) this number is added to the sentence (i)'s sentence importance score
        sentenceScores = defaultdict(int)

        for i,sentence in enumerate(sentences):
            for word in word_tokenize(sentence.lower()):
                if (word in freq):
                    sentenceScores[i] += freq[word]
        return sentenceScores

    def mainSteps(self):
        #1
        text = self.articlText
        #2
        sentences = sent_tokenize(text)
        if len(sentences) < self.n:
            self.summarizedText = "Error: Article is too small to summarize (or n is too large)"
            return
        #3
        words = word_tokenize(text.lower())
        #4
        nonStopWords = self.getNonStopwords(words)
        #5
        freq = FreqDist(nonStopWords)
        #6 (optional)
        nMostCommonWords = nlargest(10, freq, key=freq.get)
        #7
        sentenceScores = self.getSentenceRankings(sentences, freq)    
        #8
        nMostImportantSentencesIndexes = nlargest(self.n, sentenceScores, key=sentenceScores.get)
        #9
        sortedMostImportantSentencesIndexes = sorted(nMostImportantSentencesIndexes)
        #10
        summarizedSentences = ""
        for index in sortedMostImportantSentencesIndexes:
            summarizedSentences += sentences[index]
        
        self.summarizedText = summarizedSentences



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(500, 650))    
        self.setWindowTitle("Text Summarization Using a Rule Based Approach") 

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Paste Article to Summarize Here:')
        self.nameLabel.move(25, 0)
        self.nameLabel.resize(200,45)

        self.textBox = QPlainTextEdit(self)
        self.textBox.move(25, 50)
        self.textBox.resize(450, 250)

        self.textOutput = QPlainTextEdit(self)
        self.textOutput.move(25, 365)
        self.textOutput.resize(450, 250)

        

        self.pybutton = QPushButton('Summarize', self)
        self.pybutton.clicked.connect(self.clickMethod)
        self.pybutton.resize(150,32)
        self.pybutton.move(15, 320)

        self.nLabel = QLabel(self)
        self.nLabel.setText('n:')
        self.nLabel.move(185, 320)
        self.nLabel.resize(100,32)

        self.nInput = QLineEdit(self)
        self.nInput.setText("3")
        self.nInput.resize(35,32)
        self.nInput.move(200, 320)

        #pyNumber = QInputDialog.getInt(self, "Input", "n")

    def clickMethod(self):
        summarizeObject = SummarizeText(self.textBox.toPlainText(), int(self.nInput.text()))
        summarizeObject.mainSteps()
        self.textOutput.setPlainText(summarizeObject.summarizedText)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

    
