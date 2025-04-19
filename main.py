from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Railway, now with Gunicorn and logs!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting app on port {port}")
    app.run(host="0.0.0.0", port=port)
