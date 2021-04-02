

import flask
import predictPlot as pp
import predictRating as pr

app = flask.Flask(__name__)

def init():
    a = 0

@app.route('/ExistingUserPrediction')
def predictionExistingUser():
    try:
         pp.predictPlot()
    except :
        pass
    return ""

@app.route('/NewUserPrediction')
def predictionNewUser():
    try:
        pr.predictRatings()
    except :
        pass
    return ""


#app.run()