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

from functools import wraps

from flask import request
from flask import current_app

from pony.orm import ObjectNotFound

from api.server import User

from api.exceptions import TagalleryMissingLoginInformationException
from api.exceptions import TagalleryInvalidTokenException


def crypto(username, password):
    """Cypher the user password with a salt."""
    salt = username[0] + username[-1]
    cyphered = crypt.crypt(password, salt)
    return cyphered


def partition(date):
    """Return the partition directory for the image. If the partition doesn't
    exist, it will be created.

    :param date: the date the image was created.
    :type date: py:class:`datetime.datetime`

    :return: the path for the image.
    :rtype: str"""
    directory = '{base}/{year}/{month}/{day}/'.format(
        base=current_app.config['IMAGE_DIR'],
        year=date.year,
        month=date.month,
        day=date.day)

    try:
        os.makedirs(directory)
    except IOError:
        pass        # probably already exists, that's ok

    return directory


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
            try:
                user = User.get(token=token)
                if not user:
                    raise ObjectNotFound(user, 'token')
            except ObjectNotFound:
                raise TagalleryInvalidTokenException()

            result = func(*args, **kwargs)
            user.token = str(uuid.uuid4())
            result.headers.add('X-NextToken', user.token)
            return result
        return check_auth
