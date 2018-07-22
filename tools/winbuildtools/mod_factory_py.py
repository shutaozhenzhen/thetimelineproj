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


import sys
import os


CODE = """\
        import zipfile
        import sys
        import os
        path = os.path.join(os.path.split(sys.executable)[0], "library.zip")
        try:
            file = zipfile.ZipFile(path, "r")
        except:
            return []
        names = []
        for name in file.namelist():
            if name.startswith("timelinelib/plugin/plugins/"):
                name = name[27:]
                if name.endswith(".pyc") and not "__" in name:
                    name = name.split(".")[0]
                    name = name.replace("/", ".")
                    names.append(name)
        return [self._import_module("timelinelib.plugin.plugins.%s" % mod) for mod in names]        
"""


def main():
    project_dir = sys.argv[1]
    target = os.path.join(project_dir, "source", "timelinelib", "plugin", "factory.py")
    print "Script: mod2_factory_py.py"
    print "Target:", target

    f = open(target, "r")
    text = f.read()
    f.close()
    f = open(target, "w")
    lines = text.split("\n")
    state = 0
    for line in lines:
        if state == 1:
            if len(line.strip()) == 0:
                f.write(line + "\n")
                state = 0
        else:
            if "def _get_candidate_modules(self):" in line:
                f.write(line + "\n")
                f.write(CODE)
                state = 1
            else:
                f.write(line + "\n")
    f.write("\n")
    f.write("import timelinelib.plugin.plugins.eventboxdrawers.defaulteventboxdrawer\n")
    f.write("import timelinelib.plugin.plugins.eventboxdrawers.gradienteventboxdrawer\n")
    f.write("import timelinelib.plugin.plugins.eventboxdrawers.othergradienteventboxdrawer\n")
    f.write("import timelinelib.plugin.plugins.eventboxdrawers.othergradienteventboxdrawerfuzzyedges\n")
    f.write("import timelinelib.plugin.plugins.exporters.exporttobitmap\n")
    f.write("import timelinelib.plugin.plugins.exporters.exporttolist\n")
    f.write("import timelinelib.plugin.plugins.exporters.exporttosvg\n")
    f.write("import timelinelib.plugin.plugins.exporters.timelineexporter\n")

    f.close()


if __name__ == "__main__":
    main()
