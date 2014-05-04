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
import os
import os.path

from StringIO import StringIO

from base import TagalleryTests


class QueueTests(TagalleryTests):
    """Tests for the queue management."""

    @property
    def path(self):
        """Return the path for this file."""
        return os.path.dirname(inspect.getsourcefile(self.__class__))

    def setUp(self):
        self.queue_dir = os.path.join(self.path, 'images')
        super(QueueTests, self).setUp(QUEUE_DIR=self.queue_dir)
        self.user_token = self.add_user(with_token=True)
        self.test_image = 'riker.gif'
        return

    def tearDown(self):
        super(QueueTests, self).tearDown()
        uploaded_image = os.path.join(self.queue_dir, self.test_image)
        if os.path.exists(uploaded_image):
            os.unlink(uploaded_image)
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
        rv = self.get('/queue/fake_image.png', token=self.user_token)
        self.assertEqual(rv.status_code, 200)
        return

    def test_get_file_not_authd(self):
        """Try to retrieve a file without authentication."""
        rv = self.get('/queue/fake_image.png')
        self.assertJSONError(rv, 'TagalleryMissingLoginInformation')
        return

    def test_upload(self):
        """Upload a file to the queue."""
        image = file(os.path.join(self.path, 'templates', self.test_image),
                     'rb')
        rv = self.post(url='/queue/',
                       content={'image': (image, self.test_image)},
                       token=self.user_token)
        self.assertStatus(rv, 200)

        # just check if the file is there
        fullpath = os.path.join(self.queue_dir, self.test_image)
        self.assertTrue(os.path.exists(fullpath))
        return

    def test_upload_empty(self):
        """POST without a file."""
        rv = self.post(url='/queue/', content=None, token=self.user_token)
        self.assertJSONError(rv, 'TagalleryMissingFile')
        return

    def test_invalid_filetype(self):
        """Try to upload a non-image."""
        rv = self.post('/queue/',
                       content={'image': (StringIO('This is not an image'),
                                          'text.txt')},
                       token=self.user_token)
        self.assertJSONError(rv, 'TagalleryInvalidFileExtension')
        return
