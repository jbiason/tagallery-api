#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tool for managing Tagallery."""

import logging

from flask.ext.script import Manager

from api.server import app

manager = Manager(app)


# show the current configs
@manager.command
def show_config():
    """Show the current configration."""
    for key in sorted(app.config.keys()):
        print '{key}: {value}'.format(
            key=key, value=app.config[key])


# add a new administrator
@manager.command
@manager.option('-u', '--user', dest='user')
@manager.option('-p', '--password', dest='password')
def adduser(user, password):
    """Add a new administrator."""
    if not user or not password:
        print 'Username and password are required'
        return

    import crypt
    from api.server import User

    from pony.orm import db_session
    from pony.orm import commit

    salt = user[0] + user[-1]
    cyphered = crypt.crypt(password, salt)

    with db_session:
        User(login=user, password=cyphered)
        commit()


# running
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.config['DEBUG'] = True
    manager.run()
