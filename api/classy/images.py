#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Image management."""

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

import os.path
import logging
import datetime
import shutil

from flask import request
from flask import current_app
from flask import jsonify
from flask import url_for
from flask import send_from_directory

from flask.ext.classy import FlaskView

from api.database import Image

from api.utils import Auth
from api.utils import partition
from api.utils import mongoengine_to_dict

from api.exceptions import TagalleryRequestMustBeJSONException
from api.exceptions import TagalleryMissingFieldException
from api.exceptions import TagalleryNotSuchFilenameException


class ImageView(FlaskView):
    """Image management."""

    def __init__(self, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self._log = logging.getLogger('api.classy.images')
        return

    def index(self):
        """List the images."""
        # after = request.values.get('after')
        # per_page = request.values.get('ipp', 15)
        tags = request.values.get('tags', '').split(',')

        result = []
        for image in Image.objects(tags__all=tags).order_by('-created_at'):
            record = mongoengine_to_dict(image)
            record['url'] = url_for('ImageView:raw', image_id=image.id)
            result.append(record)

        return jsonify(status='OK',
                       images=result)
#   select
#       images.title
#   from
#       images,
#       tagged,
#       tags
#   where
#       images.uid == tagged.image
#       AND tagged.tag == tags.uid
#       AND tags.desc in (:list)
#   GROUP BY
#       images.title
#   HAVING
#       count(distinct tags.uid) >= :count
        raise NotImplemented

    def get(self, image_id):
        """Display a single image."""
        raise NotImplemented

    @Auth()
    def post(self):
        """Add a new image."""
        json = request.get_json(force=True, silent=True)
        if not json:
            raise TagalleryRequestMustBeJSONException()

        # the required fields
        filename = json.get('filename')
        if not filename:
            raise TagalleryMissingFieldException('filename')

        tags = json.get('tags')
        tags = self._strip_tags(json.get('tags'))
        if not tags:
            raise TagalleryMissingFieldException('tags')

        self._log.debug('Tags (as Tags): {tags}'.format(tags=tags))

        # optional fields
        title = json.get('title', '')

        # check if the file is in the queue
        queue_dir = current_app.config['QUEUE_DIR']
        in_queue = os.path.join(queue_dir, filename)
        if not os.path.exists(in_queue):
            raise TagalleryNotSuchFilenameException()

        # everything in position, try to move the file from the queue to the
        # final directory
        created_at = datetime.date.today()
        final = os.path.join(partition(created_at),
                             filename)
        shutil.move(in_queue, final)

        # save the image
        Image(title=title,
              tags=tags,
              created_at=created_at,
              filename=filename)

        return jsonify(status='OK')

    @Auth()
    def put(self, image_id):
        """Update image information."""
        raise NotImplemented

    @Auth()
    def delete(self, image_id):
        """Delete an image."""
        raise NotImplemented

    def raw(self, image_id):
        image = Image[image_id]
        final = os.path.join(partition(image.created_at),
                             image.filename)
        return send_from_directory(final)

    def _strip_tags(self, tags):
        """Make sure the tags are correct."""
        if not tags:
            raise TagalleryMissingFieldException('tags')

        tags = set([tag.strip() for tag in tags.split(',') if tag.strip()])
        if not tags:
            # there are tags, but they are empty, which basically means the
            # user just send a bunch of spaces, which is not valid
            raise TagalleryMissingFieldException('tags')

        self._log.debug('Tags: {tags}'.format(tags=tags))
        return tags
