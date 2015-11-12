# Copyright (C) 2009-2015 Contributors as noted in the AUTHORS file
#
# This file is part of timelinepackaging.
#
# timelinepackaging is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# timelinepackaging is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with timelinepackaging.  If not, see <http://www.gnu.org/licenses/>.


import os
import subprocess

import timelinepackaging.archive


class Repository(object):

    def __init__(self, root):
        self.root = root

    def archive(self, revision, destination_dir, name):
        subprocess.check_call([
            "hg", "archive",
            "-r", revision,
            "-R", self.root,
            "--no-decode",
            "--exclude", "%s/.hg*" % (self.root or "."),
            os.path.join(destination_dir, name)
        ])
        revision_hash = self._get_revision_hash(revision)
        revision_date = self._get_revision_date(revision_hash)
        archive = timelinepackaging.archive.Archive(destination_dir, name)
        archive.change_revision(revision_hash, revision_date)
        return archive

    def _get_revision_hash(self, revision):
        return subprocess.check_output([
            "hg", "id",
            "-i",
            "-r", revision,
            "-R", self.root,
        ]).strip()

    def _get_revision_date(self, revision):
        return subprocess.check_output([
            "hg", "log",
            "-r", revision,
            "-R", self.root,
            "--template", "{date|shortdate}",
        ]).strip()
