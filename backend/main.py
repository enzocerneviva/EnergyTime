from flask import Flask
from alexa_skill import alexa_webhook  # importa a função pronta

app = Flask(__name__)
app.add_url_rule("/alexa", view_func=alexa_webhook, methods=["POST"])

if __name__ == "__main__":
    from os import getenv
    port = int(getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
