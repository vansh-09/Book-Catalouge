# seed_db.py
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

# ---- Configure ----
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME   = "book_catalog"
USERNAME  = "testuser"
PASSWORD  = "testpass"   # change as you like

# ---- Script ----
bcrypt = Bcrypt()
client = MongoClient(MONGO_URI)
db     = client[DB_NAME]
users  = db["users"]

# Remove any existing testuser
users.delete_many({ "username": USERNAME })

# Generate a bcrypt hash and insert
hashed = bcrypt.generate_password_hash(PASSWORD).decode("utf-8")
users.insert_one({ "username": USERNAME, "password": hashed })

print(f"Inserted user “{USERNAME}” with bcrypt-hashed password.")