import bot
from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS, cross_origin
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/language', methods=["GET"])
@cross_origin()
def ask_language():
    if request.method == "GET":
        data = {}
        data["reply"] = "1.English  2.Arabic"
        data["status"] = 'Success'
        return jsonify(data)

@app.route('/language', methods=["POST"])
@cross_origin()
def receive_language():
    if request.method == "POST":
        request_data = request.get_json()
        message = request_data['message']
        f = open("language.txt", "w")
        if(message=="2"):
            f.write("Arabic")
            status, response = 0, "Arabic Language Selected"
        else:
            f.write("English")
            status, response = 0, "English Language Selected"
        f.close()    
        data = {}
        if status == 0:
            data["reply"] = response
            data["status"] = 'Success'
            return jsonify(data)
        else:
            data["reply"] = response
            data["status"] = 'failed'
            return jsonify(data)        

@app.route('/chat', methods=["POST"])
@cross_origin()
def chat():
    if request.method == "POST":
        request_data = request.get_json()
        message = request_data['message']
        status, response = bot.chat(message)
        data = {}
        if status == 0:
            data["reply"] = response
            data["status"] = 'Success'
            return jsonify(data)
        else:
            data["reply"] = response
            data["status"] = 'failed'
            return jsonify(data)