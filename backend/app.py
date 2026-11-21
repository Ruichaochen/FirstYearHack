import os
from flask import Flask
from flask_cors import CORS
from database import db, init_db
from routes.locations import locations_bp



app = Flask(__name__)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'locations.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_AS_ASCII"] = False  # Ensure UTF-8 characters are preserved in JSON responses

# Initialize database
init_db(app)

# Enable CORS for frontend
CORS(app)

# Register blueprints
app.register_blueprint(locations_bp)

