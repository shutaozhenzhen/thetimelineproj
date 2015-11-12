#!/usr/bin/env python
#
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


import argparse
import os
import shutil
import tempfile

from timelinepackaging import open_repository


def main():
    package_source(parse_arguments())


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=os.path.join(os.path.dirname(__file__), ".."))
    parser.add_argument("--revision", default="tip")
    parser.add_argument("--beta", action="store_true", default=False)
    return parser.parse_args()


def package_source(arguments):
    tempdir = tempfile.mkdtemp()
    try:
        create_source_zip(arguments, tempdir)
    finally:
        shutil.rmtree(tempdir)


def create_source_zip(arguments, tempdir):
    repository = open_repository(arguments.repo)
    archive = repository.archive(arguments.revision, tempdir, "archive")
    if arguments.beta:
        archive.change_version_type("TYPE_BETA")
    else:
        archive.change_version_type("TYPE_FINAL")
    archive.rename(archive.get_filename_version())
    zip_file = archive.create_zip_archive()
    extracted_archive = zip_file.extract_to(os.path.join(tempdir, "test"))
    extracted_archive.run_tests()
    zip_file.move_to_directory(".")


if __name__ == '__main__':
    main()
