import nltk
#Importing tokenization for text -> list of sentences & list of sentences -> list of words within each sentence
from nltk.tokenize import word_tokenize, sent_tokenize
#Importing stopwords
from nltk.corpus import stopwords
#Importing punctuation tokens
from string import punctuation
#Importing collocated/bigram library
from nltk.collocations import *
#Importing stemming/return word to root library
from nltk.stem.lancaster import LancasterStemmer
#Importing lexicon/thesaurus for word meanings
from nltk.corpus import wordnet as wn
#Importing algorithm to sense context/disambiguate
from nltk.wsd import lesk




text = "Michael disliked the movie Transformers. The story line was too cliche."


#1: Break up the text into a list of individual sentences
tokenizedSentences = sent_tokenize(text)



#2: Break up list of sentences into words
tokenizedWords = []
for sentence in tokenizedSentences:
    tokenizedWords.append(word_tokenize(sentence))
#print(tokenizedWords)



#3: Creating our own subset of stopwords combining 'english stopwords' and 'punctuation' as imported above
#Note: Stored in a set because order does not matter
customStopWords = set(stopwords.words('english')+list(punctuation))



#4: Filter for non stopwords from original text
nonStopWords = []
for word in word_tokenize(text):
    if(word not in customStopWords):
        nonStopWords.append(word)
#print(nonStopWords)



#5: Get bigram measures and apply (find related words in 2's)
bigram_measures = nltk.collocations.BigramAssocMeasures()
findBigrams = BigramCollocationFinder.from_words(nonStopWords)
#print(sorted(findBigrams.ngram_fd.items()))



#6: Stem/return words to their root words (in order to count frequency)
exampleText = "I drive, drove and have driven."
st = LancasterStemmer()
stemmedWords = []
for word in word_tokenize(exampleText):
    stemmedWords.append(st.stem(word))
#print(stemmedWords)



#7: Tag parts of speech
#print(nltk.pos_tag(word_tokenize(exampleText)))



#8: Word Sense Ambiguation (Find the meaning of a word in the context in which it occurs)

#The below goes through wordnet and retreives definitions for 'bark'
# for ss in wn.synsets('bark'):
#     print(ss, ss.definition())

wordContext = "I was walking by the river when I noticed some bark floating in the water."
senseResult = lesk(word_tokenize(wordContext), 'bark')
# print(senseResult, senseResult.definition())

wordContext2 = "My dog has a loud bark."
senseResult2 = lesk(word_tokenize(wordContext2), 'bark')
# print(senseResult2, senseResult2.definition())
