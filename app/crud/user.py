from app.models import User
from app.__init__ import db
from app.utils.security import generate_password_hash

def create_user(username, password):
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def update_user_password(username, new_password):
    user = get_user_by_username(username)
    if user:
        user.password_hash = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        return user
    return None

def delete_user(username):
    user = get_user_by_username(username)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

