from flask import Flask, request, jsonify
import os

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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
