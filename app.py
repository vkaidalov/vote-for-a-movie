from flask import Flask
from flask_mongoengine import MongoEngine

from api_v1 import blueprint as api_v1

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {
    "db": "vote_for_a_movie"
}
db = MongoEngine(app)

app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(debug=True)
