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
