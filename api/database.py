#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Database management."""

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

import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import ListField
from mongoengine import DateTimeField


class User(Document):
    """Users."""
    login = StringField(primary_key=True, required=True)
    password = StringField(required=True)
    last_token = StringField()


class Image(Document):
    """The images."""
    title = StringField()
    tags = ListField(StringField())
    filename = StringField()
    created_at = DateTimeField(required=True, default=datetime.datetime.utcnow)
