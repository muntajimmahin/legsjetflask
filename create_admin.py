from app import app, db, User
from werkzeug.security import generate_password_hash
with app.app_context():
    username = "admin"
    password = "admin123"
    if not User.query.filter_by(username=username).first():
        admin = User(
            username=username,
            password=generate_password_hash(password),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{username}' created.")
    else:
        print(f"User '{username}' already exists.")
