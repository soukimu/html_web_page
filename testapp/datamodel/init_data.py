# testapp/datamodel/init_data.py
import click
from flask.cli import with_appcontext
from sqlalchemy import text
from .. import db  # アプリケーションのインスタンスをインポートする

@click.command('init-users')
@with_appcontext
def init_users_command():
    with open('testapp/datamodel/init_users.sql') as f:
        data_sql = text(f.read())

    with db.engine.connect() as connection:
        connection.execute(data_sql)
    click.echo('Initialized the users in the database.')
