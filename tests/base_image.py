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
import shutil
import datetime

from base import TagalleryTests

from api.utils import partition

from api.database import Image


class BaseImage(TagalleryTests):
    """Add support for images in tests."""

    @property
    def path(self):
        """Return the path for this file."""
        return os.path.dirname(inspect.getsourcefile(self.__class__))

    def setUp(self):
        self.queue_dir = os.path.join(self.path, 'queue')
        self.image_dir = os.path.join(self.path, 'storage')
        super(BaseImage, self).setUp(QUEUE_DIR=self.queue_dir,
                                     IMAGE_DIR=self.image_dir)
        self.user_token = self.add_user(with_token=True)
        return

    def tearDown(self):
        super(BaseImage, self).tearDown()
        self._destroy_dirs()
        return

    def add_to_queue(self, filename):
        """Add an image to the image queue."""
        try:
            os.makedirs(self.queue_dir)
        except OSError:
            pass    # already exists, ignore it

        templates = os.path.join(self.path, 'images', filename)
        if not os.path.exists(templates):
            return  # you're dumb, go away

        shutil.copy(templates, self.queue_dir)
        return

    def add_to_images(self, source_filename, title=None, tags=None,
                      target_filename=None):
        """Add an image to the final directory."""
        template = os.path.join(self.path, 'images', source_filename)
        if not os.path.exists(template):
            return

        created_at = datetime.datetime.utcnow()
        final = os.path.join(partition(created_at, self.image_dir),
                             target_filename or source_filename)
        shutil.copy(template, final)

        image = Image(title=title or '',
                      tags=tags,
                      created_at=created_at,
                      filename=target_filename or source_filename)
        image.save()
        return

    def _destroy_dirs(self):
        """Destroy the paths used for queue and images created during the
        tests."""
        if os.path.exists(self.queue_dir):
            shutil.rmtree(self.queue_dir)

        if os.path.exists(self.image_dir):
            shutil.rmtree(self.image_dir)
        return
