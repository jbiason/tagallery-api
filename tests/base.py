#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Base class for testing Tagallery modules."""

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

import unittest
import uuid
import json

from pony.orm import db_session
from pony.orm import commit

from api import server

from api.utils import crypto

from api.server import User


class TagalleryTests(unittest.TestCase):
    """Base class for tagallery tests."""

    # ------------------------------------------------------------
    #  Test setup and teardown
    # ------------------------------------------------------------
    def setUp(self):
        server.db.drop_all_tables(with_all_data=True)

        server.app.config['SQLITE_FILENAME'] = ':memory:'
        server.app.config['TESTING'] = True
        server.app.config['DEBUG'] = True

        server.db.create_tables()

        self.app = server.app.test_client()
        return

    def tearDown(self):
        return

    # ------------------------------------------------------------
    #  Helpers
    # ------------------------------------------------------------
    def add_user(self, username='TestUser', password='password',
                 with_token=False):
        """Add a new user directly into the database."""
        with db_session:
            user = User(login=username, password=crypto(username, password))
            if with_token:
                user.token = str(uuid.uuid4())
            commit()

    # ------------------------------------------------------------
    #  Asserts
    # ------------------------------------------------------------
    def assertJSON(self, response, expected):
        """Assert that:

            1) The response containts a JSON response;
            2) The JSON response has all the expected fields.

        :param response: The test_client response
        :param expected: Expected JSON
        :type expected: dict"""
        response = json.loads(response.data)
        keys = expected.keys()
        for key in expected:
            if key not in response:
                self.fail('Key {key} not in response'.format(key=key))

            if response[key] != expected[key]:
                self.fail('Key {key} differs: Exepected "{expected}", '
                          'response "{response}"'.format(
                              key=key,
                              expected=expected[key],
                              response=response[key]))

            del keys[keys.index(key)]

        if keys:
            self.fail('Extraneous keys received: {keys}'.format(
                keys=', '.join(keys)))

        return

    def assertStatus(self, response, expected_status):
        """Assert that the response have the expected status"""
        self.assertEqual(response.status_code, expected_status)
        return

    def assertJSONOk(self, response, **extras):
        """Assert that the response JSON contains the "OK" status, along with
        its status. Any other fields that must be checked in the response
        should be passed in **extras."""
        expected = {'status': 'OK'}
        if extras:
            expected.update(extras)

        self.assertStatus(response, 200)
        self.assertJSON(response, expected)
        return
