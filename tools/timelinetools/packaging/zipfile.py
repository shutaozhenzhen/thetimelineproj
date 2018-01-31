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

import timelinetools.packaging.path
import timelinetools.packaging.archive


class ZipFile(timelinetools.packaging.path.Path):

    def extract_to(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        subprocess.check_call([
            "unzip",
            "-q",
            "-d", directory,
            self.get_path(),
        ])
        return timelinetools.packaging.archive.Archive(directory, self.get_basename()[:-4])
