import streamlit as st 
import pandas as pd
from pickle import load
import regex as re
from wordcloud import WordCloud

from nltk import download
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
download('wordnet') # WordNet is a lexical database for the English language that helps the script determine the base word
download('stopwords') # Stopwords are the English words which does not add much meaning to a sentence, they are ignored without sacrificing the meaning of the sentence (example, he, have, at...)
lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')


def preprocess_url(url):
    url = re.sub(r'[^a-z ]', " ", url)
    url = re.sub(r'\s+[a-zA-Z]\s+', " ", url)
    url = re.sub(r'\^[a-zA-Z]\s+', " ", url)
    url = re.sub(r'\s+', " ", url.lower())
    url = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ", url)
    return url.split()

def lemmatize_text(words, lemmatizer = lemmatizer):
    tokens = [lemmatizer.lemmatize(word) for word in words]
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [word for word in tokens if len(word) > 3]
    return tokens

def predict_spam(url):
    url = preprocess_url(url)
    url = lemmatize_text(url)
    url = [" ".join(url)]
    url = vectorizer.transform(url).toarray()
    prediction = model2.predict(url)
    return prediction

model2 = load(open('../models/spam_url_detector_svc_C-1_deg-2_gam-scale_ker-poly_42.sav', 'rb'))
vectorizer = load(open('../models/vectorizer_42.sav', 'rb'))

st.title("URL Spam Detector")
url = st.text_input("Enter a URL:")
if st.button("Predict"):
    prediction = predict_spam(url)
    if prediction == 1:
        st.write("This URL is spam")
    else:
        st.write("This URL is not spam")

