from entity.users import User  # User モデルのインポートパスを適切に設定してください
# /Users/kimurasouki/Desktop/web_page/flask/testapp/get_all_users.py
from testapp import db


def list_users():
    users = User.query.all()
    for user in users:
        print(f"Name: {user.name}, Email: {user.mail}")

if __name__ == '__main__':
    with db.app.app_context():
        list_users()