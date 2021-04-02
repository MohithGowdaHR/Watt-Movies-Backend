

import flask
import predictPlot as pp
import predictRating as pr

app = flask.Flask(__name__)

def init():
    a = 0

@app.route('/ExistingUserPrediction',methods = ['GET'])
def predictionExistingUser():
    pp.predictPlot()
    try:
         pass
    except :
        pass
    return ""

@app.route('/NewUserPrediction',methods = ['GET'])
def predictionNewUser():
    pr.predictRatings()
    try:
        pass
    except :
        pass
    return ""


#app.run()