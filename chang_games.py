import os, sys, codecs
import logging
from app import create_app, db, redis_store
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
manager = Manager(app)
migrate = Migrate(app, db, redis_store)


def make_shell_context():
    manager.add_command("shell", Shell(make_context=make_shell_context))
    manager.add_command('db', MigrateCommand)
    return dict(app=app, db=db)


if __name__ == '__main__':
    manager.run()