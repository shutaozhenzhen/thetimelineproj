#!/usr/bin/env python3
#
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


import argparse
import os
import shutil
import tempfile

import timelinetools.packaging.repository


def main():
    package_source(parse_arguments())


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", default="tip")
    return parser.parse_args()


def package_source(arguments):
    tempdir = tempfile.mkdtemp()
    try:
        create_source_zip(arguments, tempdir)
    finally:
        shutil.rmtree(tempdir)


def create_source_zip(arguments, tempdir):
    repository = timelinetools.packaging.repository.Repository()
    archive = repository.archive(arguments.revision, tempdir, "archive")
    archive.rename(archive.get_filename_version())
    archive.generate_mo_files()
    zip_file = archive.create_zip_archive()
    extracted_archive = zip_file.extract_to(os.path.join(tempdir, "test"))
    extracted_archive.execute_specs()
    zip_file.move_to_directory(".")


if __name__ == '__main__':
    main()
