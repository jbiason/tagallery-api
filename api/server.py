#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Main server code."""

# Tagallery, a tag-based web gallery
# Copyright (C) 2014  Julio Biason
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask
from flask import current_app

from mongoengine import connect

from .settings import Settings

from .exceptions import TagalleryException

# ----------------------------------------------------------------------
#  Start the app
# ----------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Settings)
app.config.from_envvar('TAGALLERY_API_CONFIG', True)

# ----------------------------------------------------------------------
#  Blueprints/Classy
# ----------------------------------------------------------------------
from classy.token import TokenView
from classy.queue import QueueView
from classy.images import ImageView

TokenView.register(app)
QueueView.register(app)
ImageView.register(app)


# ----------------------------------------------------------------------
#  Start the db before the first request
# ----------------------------------------------------------------------
@app.before_first_request
def first_request():
    init_db(current_app.config['MONGO_DB'])
    return


def init_db(db_name):
    connect(db_name)
    return


# ----------------------------------------------------------------------
#  Exceptions
# ----------------------------------------------------------------------
@app.errorhandler(TagalleryException)
def handle_tagallery_exception(error):
    return error.response()
