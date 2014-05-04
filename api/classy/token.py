#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Token generation."""

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

import uuid
import logging

from flask import request
from flask import jsonify

from flask.ext.classy import FlaskView

from pony.orm import ObjectNotFound
from pony.orm import db_session

from api.server import User

from api.utils import crypto

from api.exceptions import TagalleryMissingLoginInformationException
from api.exceptions import TagalleryNoSuchUserException


class TokenView(FlaskView):
    """Token generation requests."""

    def __init__(self, *args, **kwargs):
        super(TokenView, self).__init__(*args, **kwargs)
        self._log = logging.getLogger('api.classy.token')

    @db_session
    def get(self):
        """Return the access token. User and password must be present in the
        headers via Basic Auth."""
        self._log.debug('Authorization = {auth}'.format(
            auth=request.authorization))

        if not request.authorization:
            raise TagalleryMissingLoginInformationException()

        auth = request.authorization
        if not auth.username or not auth.password:
            raise TagalleryMissingLoginInformationException()

        cyphered = crypto(auth.username, auth.password)
        try:
            user = User.get(login=auth.username, password=cyphered)
            if not user:
                raise ObjectNotFound(User, 'login')
        except ObjectNotFound:
            self._log.debug('Cant find the user')
            raise TagalleryNoSuchUserException()

        self._log.debug('User = {user}'.format(user=user))

        token = str(uuid.uuid4())
        user.token = token

        return jsonify(status='OK',
                       token=token)
