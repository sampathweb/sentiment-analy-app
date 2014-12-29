#!/usr/bin/env python
'''Module to manage Flask Application tasks -
    Creating / Updating DB changes
    Running server locally
'''

from __future__ import print_function
import json
from flask.ext.script import Manager, Server
from app import create_app, db
from app import models

app = create_app('app.settings.Config')

manager = Manager(app)

manager.add_command("runserver", Server(use_debugger=True, use_reloader=True))


@manager.shell
def make_shell_context():
    """Creates a python REPL with several default imports in the context of the app"""
    return dict(app=app)


@manager.command
def createdb():
    """Creates a database with all of the tables defined in your Alchemy models"""
    db.create_all()


@manager.command
def seeddb(seed_file):
    data = db.session.query(models.Dataset).all()
    if len(data) > 0:
        print('DB Contains data.  Cannot import seed file')
    else:
        with open(seed_file) as f:
            data = f.read()
        seed_data = json.loads(data)
        for row in seed_data:
            dataset = models.Dataset()
            dataset.name = row['name']
            dataset.source_file = row['source_file']
            dataset.train_file = row['train_file']
            dataset.test_file = row['test_file']
            dataset.protected = True
            db.session.add(dataset)
        db.session.commit()
        print('Seed File uploaded')

if __name__ == "__main__":
    manager.run()
