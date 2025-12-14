import sys
from getpass import getpass
from app import create_app
from app.models import User, db

def create_user():
    app = create_app()
    with app.app_context():
        print("=== Create New User ===")
        username = input("Login ID (username): ").strip()
        if not username:
            print("Username is required.")
            return

        existing = User.query.filter_by(login_id=username).first()
        if existing:
            print(f"Error: User '{username}' already exists.")
            return

        name = input("Display Name: ").strip()
        password = getpass("Password: ")
        confirm = getpass("Confirm Password: ")
        
        if password != confirm:
            print("Error: Passwords do not match.")
            return

        role_input = input("Role (admin/user) [user]: ").strip().lower()
        role = "admin" if role_input == "admin" else "user"

        user = User(
            login_id=username,
            name=name,
            role=role,
            is_active=1
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        print(f"Successfully created user: {username} ({role})")

if __name__ == "__main__":
    create_user()
