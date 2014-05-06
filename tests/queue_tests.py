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

import os

from StringIO import StringIO

from base_image import BaseImage


class QueueTests(BaseImage):
    """Tests for the queue management."""

    def tearDown(self):
        super(QueueTests, self).tearDown()
        return

    def test_list(self):
        """Get a list of files in the queue."""
        self.add_to_queue('not-image.txt')
        self.add_to_queue('riker.gif')

        rv = self.get('/queue/', token=self.user_token)

        expected = {"filelist": [{"filename": "riker.gif",
                                  "url": "/queue/riker.gif"
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
        self.add_to_queue('riker.gif')
        rv = self.get('/queue/riker.gif', token=self.user_token)
        self.assertEqual(rv.status_code, 200)
        return

    def test_get_file_not_authd(self):
        """Try to retrieve a file without authentication."""
        rv = self.get('/queue/riker.gif')
        self.assertJSONError(rv, 'TagalleryMissingLoginInformation')
        return

    def test_upload(self):
        """Upload a file to the queue."""
        image = file(os.path.join(self.path, 'images', 'riker.gif'),
                     'rb')
        rv = self.post(url='/queue/',
                       content={'image': (image, 'riker.gif')},
                       token=self.user_token)
        self.assertStatus(rv, 200)

        # just check if the file is there
        fullpath = os.path.join(self.queue_dir, 'riker.gif')
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
