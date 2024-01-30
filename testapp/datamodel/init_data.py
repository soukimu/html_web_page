import click
from flask.cli import with_appcontext
from sqlalchemy import text
from testapp.entity import db  # アプリケーションのインスタンスをインポートする
from app import app


# SQLファイルの内容を読み込む
with app.open_resource('init_users.sql') as f:
    data_sql = text(f.read().decode('utf8'))

# SQLコマンドを実行する
db.engine.execute(data_sql)
click.echo('Initialized the users in the database.')
