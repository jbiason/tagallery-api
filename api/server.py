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

from datetime import datetime

from flask import Flask

from pony import orm

from .settings import Settings

from .exceptions import TagalleryException

# ----------------------------------------------------------------------
#  Start the app
# ----------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Settings)
app.config.from_envvar('TAGALLERY_API_CONFIG', True)


# ----------------------------------------------------------------------
#  Database
# ----------------------------------------------------------------------
db = orm.Database("sqlite", app.config['SQLITE_FILENAME'], create_db=True)


class Image(db.Entity):
    """Image storage."""
    #: image id
    id = orm.PrimaryKey(int)

    #: title for the image
    title = orm.Optional(unicode)

    #: list of tags for the image
    tags = orm.Set("Tag")

    #: date when the image was added to the database (not upload date)
    created_at = orm.Required(datetime)

    #: filename; does not include the image directory or the partitioning
    filename = orm.Required(str)


class Tag(db.Entity):
    """Image tags."""
    #: tag id
    id = orm.PrimaryKey(int)

    #: the tag itself
    tag = orm.Required(unicode)

    #: images with this tag
    images = orm. Set(Image)


class User(db.Entity):
    """Users."""
    #: login/username
    login = orm.Required(str, unique=True)

    #: password
    password = orm.Required(str)

    #: last token issued to this user
    token = orm.Optional(str)


if app.config['DEBUG']:
    orm.sql_debug(True)

db.generate_mapping(create_tables=True)

app.wsgi_app = orm.db_session(app.wsgi_app)


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
#  Exceptions
# ----------------------------------------------------------------------
@app.errorhandler(TagalleryException)
def handle_tagallery_exception(error):
    return error.response()
