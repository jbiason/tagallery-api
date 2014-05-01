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
    id = orm.PrimaryKey(int)
    title = orm.Optional(unicode)
    tags = orm.Set("Tag")
    created_at = orm.Required(datetime)
    filename = orm.Required(str, unique=True)


class Tag(db.Entity):
    id = orm.PrimaryKey(int)
    tag = orm.Required(unicode)
    images = orm. Set(Image)


class User(db.Entity):
    login = orm.Required(str, unique=True)
    password = orm.Required(str)


if app.config['DEBUG']:
    orm.sql_debug(True)

db.generate_mapping(create_tables=True)

# ----------------------------------------------------------------------
#  Blueprints
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
#  Exceptions
# ----------------------------------------------------------------------
@app.errorhandler(TagalleryException)
def handle_tagallery_exception(error):
    return repr(error)
