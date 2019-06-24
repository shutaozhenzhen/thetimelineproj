# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018  Rickard Lindberg, Roger Lindberg
#
# This file is part of Timeline.
#
# Timeline is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Timeline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Timeline.  If not, see <http://www.gnu.org/licenses/>.


import os
import subprocess

import timelinetools.packaging.archive


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


class Repository(object):

    def __init__(self, root=REPO_ROOT):
        self.root = root

    def archive(self, revision, destination_dir, name):
        subprocess.check_call([
            "hg", "archive",
            "-r", revision,
            "-R", self.root,
            "--exclude", "%s/.hg*" % (self.root or "."),
            os.path.join(destination_dir, name)
        ])
        (revision_hash, revision_tag) = self._get_revision_id(revision)
        revision_date = self._get_revision_date(revision_hash)
        archive = timelinetools.packaging.archive.Archive(destination_dir, name)
        archive.change_revision(revision_hash, revision_date)
        if archive.get_version_number_string() == revision_tag:
            archive.change_version_type("TYPE_FINAL")
        else:
            archive.change_version_type("TYPE_BETA")
        return archive

    def _get_revision_id(self, revision):
        parts = subprocess.check_output([
            "hg", "id",
            "-r", revision,
            "-R", self.root,
        ])
        if isinstance(parts, bytes):
            parts = parts.decode('utf-8')
        parts = parts.strip().split(" ")
        print('Revision-parts: %s' % parts)
        if len(parts) == 1:
            return (parts[0], None)
        elif len(parts) == 2:
            return (parts[0], parts[1])
        else:
            raise Exception("Unknown id %r" % (parts,))

    def _get_revision_date(self, revision):
        return subprocess.check_output([
            "hg", "log",
            "-r", revision,
            "-R", self.root,
            "--template", "{date|shortdate}",
        ]).strip()
