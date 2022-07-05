from flask import Flask,render_template, request
import re
import pandas as pd


import numpy as np
from nltk.stem.porter import *
from nltk.corpus import stopwords
import pickle

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')



# pickling the feature extraction model 
w2v_model = pickle.load(open('model_w2v.pkl', 'rb'))
# pickling model
xgb_model = pickle.load(open('dump.pkl', 'rb'))

app = Flask(__name__)

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
        
    return input_txt

def word_vector(tokens, size):
    vec = np.zeros(size).reshape((1, size))
    count = 0.
    for word in tokens:
        try:
            vec += w2v_model.wv[word].reshape((1, size))
            count += 1.
        except KeyError: # handling the case where the token is not in vocabulary
            continue
    if count != 0:
        vec /= count
    return vec

def cleaning_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in set(stopwords.words('english'))])

def preprocessData(tweet):
    # removing @ starting words
    clean_tweet = remove_pattern(tweet, "@[\w]*")
    
    # removing all special character except '#'
    clean_tweet = re.sub('[^a-zA-Z#]', ' ', clean_tweet)
#     clean_tweet = clean_tweet.replace("[^a-zA-Z#]", " ") 
    
    
    # removing short words 
    clean_tweet = ' '.join([w for w in clean_tweet.split() if len(w)>3])
    
    clean_tweet = cleaning_stopwords(clean_tweet)
    
    # text normalization
    tokenized_tweet = clean_tweet.split() # tokenizing
    
    #stemming
    stemmer = PorterStemmer()
    clean_tweet = ' '.join([stemmer.stem(i) for i in tokenized_tweet])
    
    # removing hashtag and keeping the word
    clean_tweet = clean_tweet.replace("#", "")
    
    return clean_tweet

def SentimentAnalysis(text):
        # pre-processing the raw text
        cleanedText = preprocessData(text)
        
        # feature extraction and feature selection
        tokens = cleanedText.split()
        w2v_model.train(tokens, total_examples= 1, epochs=1)
        wordvec_arrays = np.zeros((1, 200))
        wordvec_arrays = word_vector(tokens, 200)
        result = xgb_model.predict(wordvec_arrays)[0]
        
        if result == 0:
            return "positive"
        else:
            return "negative"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index', methods = ['POST', 'GET'])
def index():
    # text = str(request.form.get('data'))
    # result = SentimentAnalysis(text)
    if request.method == "POST":
        text = str(request.form.get('data'))
        sid =  SentimentIntensityAnalyzer()
        score = sid.polarity_scores(text)
        if score["neg"]!= 0:
            return render_template('index.html', result="Negative")
        else:
            return render_template('index.html', result="Positive")


    return render_template('index.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



