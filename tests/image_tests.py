#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tests for the images."""

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

import json
import urllib

from base_image import BaseImage


class ImageTests(BaseImage):
    """Tests for the image module."""

    def test_save(self):
        """Save a file from the queue to the final directory"""
        self.add_to_queue('riker.gif')
        request = {'filename': 'riker.gif',
                   'tags': 'riker,image',
                   'title': 'riker'}
        rv = self.post('/image/',
                       json.dumps(request),
                       self.user_token)
        self.assertJSONOk(rv)
        return

    def test_send_non_json(self):
        """Make a request, but don't use JSON."""
        self.add_to_queue('riker.gif')
        request = {'filename': 'riker.gif',
                   'tags': 'riker,image',
                   'title': 'riker'}
        rv = self.post('/image/',
                       urllib.urlencode(request),
                       self.user_token)
        self.assertJSONError(rv, 'TagalleryRequestMustBeJSON')
        return

    def test_no_filename(self):
        """Send a request without the filename."""
        request = {'tags': 'riker,image',
                   'title': 'riker'}
        rv = self.post('/image/',
                       json.dumps(request),
                       self.user_token)
        self.assertJSONError(rv, 'TagalleryMissingField')
        return

    def test_no_tags(self):
        """Send a request without the tags."""
        request = {'filename': 'riker.gif',
                   'title': 'riker'}
        rv = self.post('/image/',
                       json.dumps(request),
                       self.user_token)
        self.assertJSONError(rv, 'TagalleryMissingField')
        return

    def test_empty_tags(self):
        """Send a request with tags, but all empty."""
        request = {'filename': 'riker.gif',
                   'tags': ',',
                   'title': 'riker'}
        rv = self.post('/image/',
                       json.dumps(request),
                       self.user_token)
        self.assertJSONError(rv, 'TagalleryMissingField')
        return

    def test_blank_tags(self):
        """Send a request with tags, but all blank (spaces)."""
        request = {'filename': 'riker.gif',
                   'tags': '   ,    ',
                   'title': 'riker'}
        rv = self.post('/image/',
                       json.dumps(request),
                       self.user_token)
        self.assertJSONError(rv, 'TagalleryMissingField')
        return

    def test_no_such_file(self):
        """Try to save a file that it is not in the queue."""
        request = {'filename': 'riker.gif',
                   'tags': 'riker,image',
                   'title': 'riker'}
        rv = self.post('/image/',
                       json.dumps(request),
                       self.user_token)
        self.assertJSONError(rv, 'TagalleryNotSuchFilename')
        return

    def test_index(self):
        """Try to get the index."""
        self.add_to_images('riker.gif', tags=['gif', 'riker'])
        self.add_to_images('riker.gif', tags=['gif', 'riker'],
                           target_filename='riker1.gif')
        rv = self.get('/image/')
        self.assertJSONOk(rv)

        data = json.loads(rv.data)
        self.assertTrue(len(data['images']) == 2)

        # because riker1 was created last, it should be the first in the
        # results
        self.assertTrue(data['images'][0]['filename'] == 'riker1.gif')
        self.assertTrue(data['images'][1]['filename'] == 'riker.gif')
        return
