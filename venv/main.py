import bot
from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS, cross_origin
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def hello_world():
    return 'Hello, World!'

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