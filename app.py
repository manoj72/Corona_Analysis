from flask import Flask,render_template,request
import pickle
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import os
from twilio.rest import Client
import requests
def notification(num, sms):
    number='+91'+num
    account_sid = "ACbcbf466dfaffd76b75faeef2a3e9cb13"
    auth_token = 'd2aefd97a262b8dc536f0be76656356d'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=number,
        from_="+18183304193",
        body=sms)
app = Flask(__name__)
@app.route('/')
def home_page():
    return render_template('home.html')
@app.route('/prediction' , methods=['POST'])
def prediction():
    if request.method=='POST':
        Name = request.form['name']
        Number = request.form['number']
        Age=request.form['age']
        Fever=request.form['fever']
        Breath = request.form['breath']
        Cold = request.form['cold']
        Body = request.form['body']
        pkl1=pickle.load(open("coronaPredict.pkl" , "rb"))
        # columns  -- Age,	Fever,	BodyPains,	RunnyNose,	Difficulty_in_Breath
        data = [[int(Age), int(Fever), int(Body), int(Cold), int(Breath)]]
        predict = pkl1.predict(data)[0]
        proba_score = pkl1.predict_proba([[60, 100, 0, 1, 0]])[0][0]

        if predict == 1:
            prediction = 'Positive'
            sms = Name + "your report is" + prediction + "that means you have corona syntams to please go and do your covid test to secure yourself and your family"
        else:
            prediction = 'Negative'
            sms = Name + "your report is" + prediction + " you don`t have any corona syntams so you are save enjoy"
        notification(Number, sms)
        return render_template('home.html', prediction=prediction, proba_score=round(proba_score * 100, 2))
    else:
        return render_template('home.html', message='Something missed, Please follow the instructions..!')


if __name__ == '__main__':
    app.run(debug=True)