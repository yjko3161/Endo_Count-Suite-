from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
bcrypt = Bcrypt(app)

target_hash = "$2b$12$KAwp1k453dQT4F3Ca.ci9u.LucPzKhhCxpCzTjhxqm8ffNa1FAeua"
candidates = ["changeme", "admin", "1234", "password", "user", "test"]

print(f"Checking hash: {target_hash}")
for p in candidates:
    if bcrypt.check_password_hash(target_hash, p):
        print(f"MATCH FOUND: The password is '{p}'")
        exit(0)

print("No match found in common defaults.")
