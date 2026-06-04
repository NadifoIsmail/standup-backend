from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
import os

from models import db
from routes import standup_bp
from flask import send_from_directory


app = Flask(__name__)

# # DATABASE CONFIG
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///standups.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# IN PRODUCTION
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# FILE UPLOAD FOLDER
app.config["UPLOAD_FOLDER"] = "uploads"

# ENABLE CORS
CORS(app)

# INITIALIZE DATABASE
db.init_app(app)

# MIGRATIONS
migrate = Migrate(app, db)

# REGISTER ROUTES
app.register_blueprint(standup_bp)

@app.route("/")
def home():
    return "Standup Logger API Running"

@app.route('/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory('uploads', filename)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)