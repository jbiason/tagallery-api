#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Image functions."""

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

import inspect
import os.path

from base import TagalleryTests


class BaseImage(TagalleryTests):
    """Add support for images in tests."""

    @property
    def path(self):
        """Return the path for this file."""
        return os.path.dirname(inspect.getsourcefile(self.__class__))

    def setUp(self):
        self.queue_dir = os.path.join(self.path, 'images')
        super(BaseImage, self).setUp(QUEUE_DIR=self.queue_dir)
        self.user_token = self.add_user(with_token=True)
        self.test_image = 'riker.gif'
        return
