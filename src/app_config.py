import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=BASE_DIR)

# Get the underlying Flask app instance
app = connex_app.app

# Build the Sqlite URL for SqlAlchemy
sqlite_url = "sqlite:///" + os.path.join(BASE_DIR, "dekh_tamasha.db")

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)
