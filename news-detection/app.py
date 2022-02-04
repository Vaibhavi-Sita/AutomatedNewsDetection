'''
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import pickle
from flask import Flask, jsonify    
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/checknews/<var>", methods=["GET"])
def detecting_fake_news(var):


    df = pd.read_csv('corona_fake.csv')
    print(df.shape)

    df = df.fillna('')

    df['title_text_source'] = df['title'] + ' ' + df['text'] + ' ' + df['source']

    df = df[df['label']!='']
    print(df['label'].unique())

    df.loc[df['label'] == 'fake', 'label'] = 'FAKE'
    df.loc[df['label'] == 'Fake', 'label'] = 'FAKE'

    no_of_fakes = df.loc[df['label'] == 'FAKE'].count()[0]
    no_of_trues = df.loc[df['label'] == 'TRUE'].count()[0]

    stop_words = set(stopwords.words('english'))
    def clean(text):
        # Lowering letters
        text = text.lower()
        
        # Removing html tags
        text = re.sub(r'<[^>]*>', '', text)
        
        # Removing twitter usernames
        text = re.sub(r'@[A-Za-z0-9]+','',text)
        
        # Removing urls
        text = re.sub('https?://[A-Za-z0-9]','',text)
        
        # Removing numbers
        text = re.sub('[^a-zA-Z]',' ',text)
        
        word_tokens = word_tokenize(text)
        
        filtered_sentence = []
        for word_token in word_tokens:
            if word_token not in stop_words:
                filtered_sentence.append(word_token)
        
        # Joining words
        text = (' '.join(filtered_sentence))
        return text

    df['title_text_source'] = df['title_text_source'].apply(clean)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['title_text_source'].values)
    X = X.toarray()

    y = df['label'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=0.2, random_state=11)

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    #print(clf.score(X_train, y_train))
    #print(clf.score(X_test, y_test))

    #predictions = clf.predict(X_test)

    
    cm = confusion_matrix(y_test, predictions)

    plt.figure(figsize=(6,6))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=['FAKE', 'TRUE'], yticklabels=['FAKE', 'TRUE'], cmap=plt.cm.Blues, cbar=False)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()

    sentence = 'The Corona virus is a man made virus created in a Wuhan laboratory. Doesn’t @BillGates finance research at the Wuhan lab?'
    sentence = clean(sentence)
    vectorized_sentence = vectorizer.transform([sentence]).toarray()
    clf.predict(vectorized_sentence)
    

    sentence = var
    sentence = clean(sentence)
    vectorized_sentence = vectorizer.transform([sentence]).toarray()
    result = clf.predict(vectorized_sentence)

    return result[0]

'''

import pickle
from flask import Flask, jsonify    
from flask_cors import CORS, cross_origin
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

app = Flask(__name__)
CORS(app)



@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/checknews/<var>", methods=["GET"])
def detecting_fake_news(var):

    train = [
    ('Says the Annies List political group supports third-trimester abortions on demand.', 'false'),
    ('Donald Trump is against marriage equality. He wants to go back.', 'true'),
    ('Says nearly half of Oregons children are poor.', 'true'),
    ('State revenue projections have missed the mark month after month.', 'true'),
    ("In the month of January, Canada created more new jobs than we did.", 'true'),
    ('If people work and make more money, they lose more in benefits than they would earn in salary.', 'false'),
    ('Originally, Democrats promised that if you liked your health care plan, you could keep it. One year later we know that you need a waiver to keep your plan.', 'false'),
    ("We spend more money on antacids than we do on politics.", 'false'),
    ('Barack Obama and Joe Biden oppose new drilling at home and oppose nuclear power.', 'false'),
    ('President Obama once said he wants everybody in America to go to college.', 'false'),
    ('Yogi inaugurates Kashi', 'false'),
    ('Telangana reports Omicron cases', 'true'),
    ('PM Modi inaugurates Kashi Vishwanath corridor in Varanasi', 'true'),
    ('Yogi Adityanath inaugurates Kashi Vishwanath corridor in Varanasi', 'false')
    ]
    test = [
    ('Because of the steps we took, there are about 2 million Americans working right now who would otherwise be unemployed.', 'true'),
    ("You cannot build a little guy up by tearing a big guy down -- Abraham Lincoln said it.", 'false'),
    ("One man opposed a flawed strategy in Iraq. One man had the courage to call for change. One man didn't play politics with the truth.", 'true'),
    ('When I was governor, not only did test scores improve we also narrowed the achievement gap.', 'true'),
    ('Telangana reports Omicron cases', 'true'),
    ("Ukraine was a nuclear-armed state. They gave away their nuclear arms with the understanding that we would protect them.", 'false')
    ]   

    cl = NaiveBayesClassifier(train)
    result = cl.classify(var) 

    return result



if __name__ == "__main__":
    app.run(debug=True)

