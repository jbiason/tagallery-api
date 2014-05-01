#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Server exceptions."""

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

from flask import jsonify


class TagalleryException(Exception):
    """Generic/base exception."""
    def __init__(self):
        self.status = 500
        self.message = 'Unknown error'

    def json(self):
        """Convert the error information to JSON. If you need to add more
        information or something, override this method."""
        code = self.__class__.__name__[:-9]     # remove "Exception"
        return {'status': 'ERROR',
                'message': self.message,
                'code': code}

    def __repr__(self):
        """Exception representation. Returns the exception in JSON format."""
        response = jsonify(self.json())
        response.status_code = self.status
        return response
