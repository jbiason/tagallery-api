#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Manage the image queue."""

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
import logging

from flask import current_app
from flask import url_for
from flask import jsonify
from flask import send_from_directory

from flask.ext.classy import FlaskView

from api.utils import Auth


class QueueView(FlaskView):
    """Queue management requests."""

    def __init__(self, *args, **kwargs):
        super(QueueView, self).__init__(*args, **kwargs)
        self.log = logging.getLogger('api.classy.queue')

    @Auth()
    def index(self):
        """Return the list of files in the queue."""
        queue_dir = current_app.config['QUEUE_DIR']
        extensions = current_app.config['IMAGE_EXTENSIONS']

        filelist = []
        for filename in os.listdir(queue_dir):
            self.log.debug('Found file {filename}'.format(filename=filename))
            matches = [filename.lower().endswith(ext) for ext in extensions]
            if not any(matches):
                self.log.debug('... ignored')
                continue

            filelist.append({'filename': filename,
                             'url': url_for('QueueView:get',
                                            filename=filename)})

        return jsonify(status='OK',
                       filelist=filelist)

    @Auth()
    def get(self, filename):
        """Serve a file directly from the queue."""
        queue_dir = current_app.config['QUEUE_DIR']
        return send_from_directory(queue_dir, filename)
