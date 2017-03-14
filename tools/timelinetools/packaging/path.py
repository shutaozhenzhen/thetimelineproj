# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg
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
import shutil


class Path(object):

    def __init__(self, dirname, basename):
        self._dirname = dirname
        self._basename = basename

    def get_dirname(self):
        return self._dirname

    def get_basename(self):
        return self._basename

    def get_path(self):
        return os.path.join(self._dirname, self._basename)

    def rename(self, new_basename):
        os.rename(self.get_path(), os.path.join(self._dirname, new_basename))
        self._basename = new_basename

    def move_to_directory(self, directory):
        destination = os.path.join(directory, self.get_basename())
        shutil.move(self.get_path(), destination)
        self.parent_dir = os.path.abspath(directory)
