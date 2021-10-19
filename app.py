# Application Entrypoint

# Flask
from flask import Flask
from flask_restful import Api

# Utils
import os

app = Flask(__name__)
api = Api(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
