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
import timelinepackaging.path


class ZipFile(timelinepackaging.path.Path):

    def extract_to(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        subprocess.check_call([
            "unzip",
            "-q",
            "-d", directory,
            self.get_path(),
        ])
        return timelinepackaging.archive.Archive(directory, self.get_basename()[:-4])
