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

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.config['DEBUG'] = True
    manager.run()
