import numpy as np
import pandas as pd
import joblib

from tensorflow.keras.models import load_model
from flask import Flask, render_template, request
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import StandardScaler
from joblib import dump, load
from tensorflow.keras.models import load_model

scaler = load('models/scaler.joblib')
rf_model = joblib.load('models/randomForest_model.sav')
log_reg = joblib.load('models/logisticReg_model.sav')
dt_model = joblib.load('models/decision_tree_model.sav')
svc_model = joblib.load('models/svc_model.sav')
xgb_model = joblib.load('models/xgb_model.sav')
nn_model = load_model("models/diabetes_neuralnet.h5")

# Flask constructor
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/data', methods=["GET", "POST"])
def data():
    response = request.form
    age = float(response['age'])
    bmi = float(response['bmi'])
    glu = float(response['glucose'])
    ins = float(response['insulin'])
    bp = float(response['blood pressure'])
    skth = float(response['skin thickness'])
    dpf = float(response['diabetes pedigree function'])/1000
    preg = float(response['pregnancies'])

    X = np.array([preg, glu, bp, skth, ins, bmi, dpf, age])
    reX = X.reshape(1, -1)
    X_scaled = scaler.transform(reX)

    yPre = rf_model.predict(X_scaled)
    yPre_lg = log_reg.predict(X_scaled)
    yPre_dt = log_reg.predict(X_scaled)
    yPre_svc = log_reg.predict(X_scaled)
    yPre_xgb = log_reg.predict(X_scaled)
    yPre_nn = nn_model.predict(X_scaled)

    response_data = {
        'Random Forest:': yPre,
        'Logistic Regression:': yPre_lg,
        'Decision Tree:': yPre_dt,
        'Support Vector Model:': yPre_svc,
        'Xtreme Gradient Boosting:': yPre_xgb,
        'Neural Network': yPre_nn
    }

    return render_template("data.html", response=response_data)


@app.route('/glucose')
def glucose():
    return render_template("glucose.html")


@app.route('/age')
def age():
    return render_template("age.html")


@app.route('/scatter')
def scatter():
    return render_template("scatter.html")


@app.errorhandler(400)
def bad_request(e):
    # note that we set the 400 status explicitly
    return render_template('400.html'), 400


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
