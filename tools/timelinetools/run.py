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


import subprocess
import sys


def run_python_script_and_exit_if_fails(path, args=[], cwd=None):
    run_cmd_and_exit_if_fails([sys.executable, path] + args, cwd=cwd)


def run_cmd_and_exit_if_fails(cmd, cwd=None):
    try:
        subprocess.check_call(cmd, cwd=cwd)
    except subprocess.CalledProcessError:
        sys.exit(1)
