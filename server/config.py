class Config:
    SECRET_KEY = "super-secret-key"  # Used for session security and password hashing
    SQLALCHEMY_DATABASE_URI = "sqlite:///finance.db"  # Tells SQLAlchemy to use a local SQLite file
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Turns off unnecessary change tracking to save resources
    JWT_SECRET_KEY = "jwt-secret"  # Secret for signing JWT tokens (needed for login auth)
