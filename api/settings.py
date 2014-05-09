#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Default settings (and general documentation about the API settings.)"""

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


class Settings(object):
    """API settings."""
    #: Enable debugging mode, defaults to False
    DEBUG = False

    #: Enable testing mode, defaults to False
    TESTING = False

    #: Path where the queued images are located; this is also the directory
    #: where upload pictures will be stores till they are properly tagged and
    #: uploaded
    QUEUE_DIR = ''

    #: Path where the images are stored; this should, for better performance,
    #: be a directory inside your "static" path
    IMAGE_DIR = ''

    #: File extensions to be considered an image while scanning the queue
    #: directory
    IMAGE_EXTENSIONS = ['jpeg', 'jpg', 'gif', 'png']

    #: Mongo Database
    MONGO_DB = 'tagallery'
