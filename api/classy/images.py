#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Image management."""

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

import logging

from flask.ext.classy import FlaskView

from api.utils import Auth


class ImageView(FlaskView):
    """Image management."""

    def __init__(self, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self._log = logging.getLogger('api.classy.images')
        return

    def index(self):
        """List the images."""
        raise NotImplemented

    def get(self, image_id):
        """Display a single image."""
        raise NotImplemented

    @Auth()
    def post(self):
        """Add a new image."""
        raise NotImplemented

    @Auth()
    def put(self, image_id):
        """Update image information."""
        raise NotImplemented

    @Auth()
    def delete(self, image_id):
        """Delete an image."""
        raise NotImplemented
