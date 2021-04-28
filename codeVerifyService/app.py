from flask import Flask, request,jsonify
from recognition import predict
app = Flask(__name__)

@app.route("/verify")
def verify():
    file = request.files['pic']
    file.save('../tmp/tmp.jpg')
    res = predict('../tmp/tmp.jpg')
    return jsonify({"code":200,"msg":"success","data":{"code":res}})
if __name__ == '__main__':

    app.run(host="0.0.0.0",port=8888)