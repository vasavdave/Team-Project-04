from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.preprocessing import StandardScaler
from joblib import dump, load
scaler = load('scaler.joblib') 
rf_model = joblib.load('randomForest_model.sav')
log_reg = joblib.load('logisticReg_model.sav')
dt_model = joblib.load('decision_tree_model.sav')
svc_model = joblib.load('svc_model.sav')
xgb_model = joblib.load('xgb_model.sav')


# from tensorflow.keras.models import load_model
# nn_model = load_model("diabetes_neuralnet.h5")

# Flask constructor
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/data', methods=["GET", "POST"])
def data():
    form_data = request.form
    age = float(form_data['age'])
    bmi = float(form_data['bmi'])
    glu = float(form_data['glucose'])
    ins = float(form_data['insulin'])
    bp = float(form_data['blood pressure'])
    skth = float(form_data['skin thickness'])
    dpf = float(form_data['diabetes pedigree function'])/1000
    preg = float(form_data['pregnancies'])
    
    X = np.array([preg,glu,bp,skth,ins,bmi,dpf,age])
    reX = X.reshape(1,-1)
    X_scaled = scaler.transform(reX)
    
    yPre = rf_model.predict(X_scaled)
    print('Random Forest Prediction: ', yPre)
    yPre_lg = log_reg.predict(X_scaled)
    print('Logistical Regression Prediction: ', yPre_lg)
    yPre_dt = log_reg.predict(X_scaled)
    print(f'Decision Tree Prediction: {yPre_dt}')
    yPre_svc = log_reg.predict(X_scaled)
    print(f'Support Vector Classifier Prediction: {yPre_svc}')
    yPre_xgb = log_reg.predict(X_scaled)
    print(f'The XG Boost Prediction: {yPre_xgb}')


    # yPre_nn = nn_model.predict(X_scaled)
    # print('Neural Network Prediction: ', yPre_nn)
    temp = [yPre, yPre_lg]

 #   form_data = [('age',age),('bmi',bmi),('glucoes',glu),('insulin',ins),('blood pressure',bp),('skin thickness',skth),('diabetes predigree function',dpf),('pregnancies',preg)]

    #print(type(form_data))

    return render_template("data.html", form_data=temp)


if __name__ == '__main__':
    app.run()
