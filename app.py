from flask import Flask, render_template, request, jsonify
# from chatbot import get_response
from flask_cors import CORS
from chatbot import get_response_json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.post("/predict")
def predict():
    sentence = request.get_json().get("message")
    #TODO: check if text is valid
    response = get_response_json(sentence)
    # message = {"answer": response}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
