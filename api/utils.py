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

from functools import wraps

from flask import request

from pony.orm import ObjectNotFound

from api.server import User

from api.exceptions import TagalleryMissingLoginInformationException
from api.exceptions import TagalleryInvalidTokenException


def crypto(username, password):
    """Cypher the user password with a salt."""
    salt = username[0] + username[-1]
    cyphered = crypt.crypt(password, salt)
    return cyphered


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
