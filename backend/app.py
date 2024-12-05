from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    instance_id = os.getenv("INSTANCE_ID", "unknown")
    return f"Hello from backend instance {instance_id}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
