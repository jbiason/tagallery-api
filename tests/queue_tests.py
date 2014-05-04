#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tests for the queue."""

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


class QueueTests(TagalleryTests):
    """Tests for the queue management."""

    def setUp(self):
        file_path = os.path.dirname(inspect.getsourcefile(self.__class__))
        queue_dir = os.path.join(file_path, 'images')
        super(QueueTests, self).setUp(QUEUE_DIR=queue_dir)

        self.user_token = self.add_user(with_token=True)
        return

    def test_list(self):
        """Get a list of files in the queue."""
        rv = self.get('/queue/', token=self.user_token)

        expected = {"filelist": [{"filename": "fake_image.png",
                                  "url": "/queue/fake_image.png"
                                  }
                                 ]}
        self.assertJSONOk(rv, **expected)
        return

    def test_not_auth(self):
        """Try to get the list without being authenticated."""
        rv = self.get('/queue/')
        self.assertJSONError(rv, 'TagalleryMissingLoginInformation')
        return

    def test_get_file(self):
        """Try to retrieve a file."""
        rv = self.get('/queue/fake_image.png')
        self.assertEqual(rv.status_code, 200)
        return
