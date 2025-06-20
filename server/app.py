from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import db
from auth import auth_bp
from transactions import transactions_bp


app = Flask(__name__)
app.config.from_object(Config)
app.config["JWT_SECRET_KEY"] = "your-secret-key"

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

print("✅ Flask has started. 1..")

app.register_blueprint(auth_bp)
app.register_blueprint(transactions_bp)
print("✅ Flask has started 2...")

@app.route("/")
def home():
    return {"message": "Finance Tracker API"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables just once, on app startup
    app.run(debug=True)
