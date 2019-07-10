from flask import Flask, request, jsonify
import pickle
app = Flask(__name__)
cv = pickle.load(open('cv.pkl','rb'))
lr = pickle.load(open('lr.pkl','rb'))

@app.route("/")
def hello():
    return u"Hello world!"

@app.route("/vova")
def hello_vova():
    return u"Hello Vova!"

@app.route("/predict")
def predict():
    try:
        x1 = float(request.args.get('x1',0))
        x2 = float(request.args.get('x2',0))
        return u"Result: {}".format(x1*x2)
    except:
        return "Фигня"

@app.route("/predict_mov")
def predict_mov():
    txt = request.args.get('text',0)
    return str(lr.predict_proba(cv.transform([txt]))[0][1])

@app.route("/predict_new", methods=['POST'])
def predict_new():
    txt = request.form.get('text',0)
    if txt is None:
        txt = request.args.get('text',0)
    resp = {'proba':lr.predict_proba(cv.transform([txt]))[0][1],
            'text':txt}
    return jsonify(resp)

app.run(port=5000, debug=True)