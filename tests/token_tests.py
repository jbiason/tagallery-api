#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Tests for token."""

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

import base64
import unittest
import json

from base import TagalleryTests


class TokenTests(TagalleryTests):
    """Tests for tokens."""

    def test_get_token(self):
        """Try to get a token."""
        self.add_user(username='test', password='test')

        message = 'test:test'
        headers = {'Authorization': 'Basic {code}'.format(
            code=base64.b64encode(message))}

        rv = self.app.get('/token/', headers=headers)
        self.assertJSONOk(rv)

        data = json.loads(rv.data)
        self.assertTrue('token' in data)
        return


if __name__ == '__main__':
    unittest.main()
