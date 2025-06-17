from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/alexa", methods=["POST"])
def alexa_webhook():
    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Teste básico OK!"
            },
            "shouldEndSession": True
        }
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
