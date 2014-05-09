#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Utility functions."""

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

import crypt
import uuid
import os
import logging

from functools import wraps

from flask import request
from flask import current_app

from bson.objectid import ObjectId

from mongoengine.base import BaseList

from api.database import User

from api.exceptions import TagalleryMissingLoginInformationException
from api.exceptions import TagalleryInvalidTokenException


LOG = logging.getLogger('api.utils')


def crypto(username, password):
    """Cypher the user password with a salt."""
    salt = username[0] + username[-1]
    cyphered = crypt.crypt(password, salt)
    return cyphered


def partition(date, base=None):
    """Return the partition directory for the image. If the partition doesn't
    exist, it will be created.

    :param date: the date the image was created.
    :type date: py:class:`datetime.datetime`
    :param base: the base directory to create the partition; if None, the
                 IMAGE_DIR configuration will be used
    :type base: str

    :return: the path for the image.
    :rtype: str"""
    if not base:
        base = current_app.config['IMAGE_DIR']

    directory = '{base}/{year:04}/{month:02}/{day:02}/'.format(
        base=base,
        year=date.year,
        month=date.month,
        day=date.day)

    try:
        os.makedirs(directory)
    except OSError:
        pass        # probably already exists, that's ok

    return directory


def mongoengine_to_dict(doc):
    """Convert a mongoengine document to a python dictionary."""
    result = {}
    # LOG.debug('Doc: {doc}'.format(doc=doc))
    for field in doc:
        value = getattr(doc, field)
        # LOG.debug('field: {field}/{value}'.format(
        #     field=field, value=value))

        if isinstance(value, BaseList):
            records = []
            for record in value:
                records.append(record)
            value = records

        elif isinstance(value, ObjectId):
            value = str(value)

        result[field] = value
    return result


class Auth(object):
    """Decorator for forcing authentication in the request."""
    def __call__(self, func):
        @wraps(func)
        def check_auth(*args, **kwargs):
            if not request.authorization:
                raise TagalleryMissingLoginInformationException()

            # request informatino requires that the user in the basic auth is,
            # actually, the token
            token = request.authorization.username
            user = User.objects(last_token=token).first()
            if not user:
                raise TagalleryInvalidTokenException()

            result = func(*args, **kwargs)
            user.last_token = str(uuid.uuid4())
            result.headers.add('X-NextToken', user.last_token)
            return result
        return check_auth
