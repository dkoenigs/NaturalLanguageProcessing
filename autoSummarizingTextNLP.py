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


def getUrlText(articleUrl):
    http = urllib3.PoolManager()
    response = http.request('GET', articleUrl)
    soup = BeautifulSoup(response.data, features="html.parser")
    textOnly = soup.find(class_= 'entry-content').text
    return textOnly

def getNonStopwords(words):
    stopWords = set(stopwords.words('english') + list(punctuation))
    nonStopWords = []
    for word in words:
        if word not in stopWords:
            nonStopWords.append(word)
    return nonStopWords

def getSentenceRankings(sentences, freq):
    #For each sentence (i) go through all words in the sentence and look up how often it
    #occurs in the text overall (freq) this number is added to the sentence (i)'s sentence importance score
    sentenceScores = defaultdict(int)

    for i,sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if (word in freq):
                sentenceScores[i] += freq[word]
    return sentenceScores

def mainSteps(articleUrl, n):
    #1
    text = getUrlText(articleUrl)
    #2
    sentences = sent_tokenize(text)
    if len(sentences) < n:
        return "Error: Article is too small to summarize (or n is too large)"
    #3
    words = word_tokenize(text.lower())
    #4
    nonStopWords = getNonStopwords(words)
    #5
    freq = FreqDist(nonStopWords)
    #6 (optional)
    nMostCommonWords = nlargest(10, freq, key=freq.get)
    #7
    sentenceScores = getSentenceRankings(sentences, freq)    
    #8
    nMostImportantSentencesIndexes = nlargest(n, sentenceScores, key=sentenceScores.get)
    #9
    sortedMostImportantSentencesIndexes = sorted(nMostImportantSentencesIndexes)
    #10
    summarizedSentences = ""
    for index in sortedMostImportantSentencesIndexes:
        summarizedSentences += sentences[index]
    return summarizedSentences




def main():
    articleUrl = "https://fs.blog/2019/10/focused-diffuse-thinking/"
    summarizedText = mainSteps(articleUrl, 100)
    print(summarizedText)


if __name__ == "__main__":
    main()