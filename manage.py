#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tool for managing Tagallery."""

import logging

from flask.ext.script import Manager

from api.server import app

manager = Manager(app)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.config['DEBUG'] = True
    manager.run()
