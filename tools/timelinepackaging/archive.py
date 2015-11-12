# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015  Rickard Lindberg, Roger Lindberg
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
import re
import subprocess
import sys

import timelinepackaging.path
import timelinepackaging.zipfile


class Archive(timelinepackaging.path.Path):

    def change_revision(self, revision_hash, revision_date):
        self._change_version_constant("REVISION_HASH", "\"%s\"" % revision_hash)
        self._change_version_constant("REVISION_DATE", "\"%s\"" % revision_date)

    def change_version_type(self, version_type):
        self._change_version_constant("TYPE", version_type)
        _make_one_sub(
            self._get_readme_path(),
            r"^(This directory contains the ).*( version of Timeline.)$",
            r"\g<1>%s\g<2>" % self.get_readme_version()
        )

    def get_filename_version(self):
        return subprocess.check_output([
            sys.executable,
            "-c",
                "import timelinelib.meta.version;"
                "print(timelinelib.meta.version.get_filename_version());"
        ], cwd=self._get_source_path()).strip()

    def get_readme_version(self):
        return subprocess.check_output([
            sys.executable,
            "-c",
                "import timelinelib.meta.version;"
                "print(timelinelib.meta.version.get_readme_version());"
        ], cwd=self._get_source_path()).strip()

    def run_tests(self):
        subprocess.check_call([
            sys.executable,
            os.path.join("test", "execute-specs.py"),
        ], cwd=self.get_path())

    def create_zip_archive(self):
        self._clean_pyc_files()
        zip_name = "%s.zip" % self.get_basename()
        subprocess.check_call([
            "zip",
            "--quiet",
            "--recurse-paths",
            zip_name,
            self.get_basename(),
        ], cwd=self.get_dirname())
        return timelinepackaging.zipfile.ZipFile(self.get_dirname(), zip_name)

    def _change_version_constant(self, constant, value):
        _change_constant(self._get_version_path(), constant, value)
        self._clean_pyc_files()

    def _clean_pyc_files(self):
        for root, dirs, files in os.walk(self.get_path()):
            for f in files:
                if f.endswith(".pyc"):
                    os.remove(os.path.join(root, f))

    def _get_readme_path(self):
        return os.path.join(self.get_path(), "README")

    def _get_version_path(self):
        return os.path.join(self._get_source_path(), "timelinelib", "meta", "version.py")

    def _get_source_path(self):
        return os.path.join(self.get_path(), "source")


def _change_constant(path, constant, value):
    _make_one_sub(
        path,
        r"^%s\s*=\s*.*?$" % constant,
        "%s = %s" % (constant, value)
    )


def _make_one_sub(path, regex, replacement):
    with open(path) as f:
        content = f.read()
    (new_content, number_of_subs_made) = re.subn(
        regex,
        replacement,
        content,
        flags=re.MULTILINE
    )
    if number_of_subs_made != 1:
        raise ValueError("Expected 1 sub but got %d: %s %s" % (
            number_of_subs_made,
            path,
            constant
        ))
    with open(path, "w") as f:
        f.write(new_content)
