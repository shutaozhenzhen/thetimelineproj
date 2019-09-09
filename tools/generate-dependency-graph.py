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


import os
import re
import sys

from timelinetools.paths import SOURCE_DIR


def generate_dependency_graph(module_prefix):
    dot = Dot()
    dot.start()
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".py"):
                for module, dependency in extract_dependencies(os.path.join(root, file)):
                    if (dependency.startswith("timelinelib") and
                        module.startswith(module_prefix)):
                        dot.dependency(module, dependency)
    dot.end()


def extract_dependencies(path):
    IMPORT_RES = [
        re.compile(r"^\s*from\s(.+?)\simport\s"),
        re.compile(r"^\s*import\s(.+?)(\sas\s.+?)?$"),
    ]
    with open(path) as f:
        for line in f:
            for import_re in IMPORT_RES:
                match = import_re.search(line)
                if match:
                    yield module_name(path), match.group(1)


def module_name(path):
    name = path
    name = os.path.relpath(name, SOURCE_DIR)
    name = rstrip(name, ".py")
    name = rstrip(name, "/__init__")
    name = name.replace("/", ".")
    return name


def rstrip(string, what):
    if string.endswith(what):
        return string[:-len(what)]
    return string


def get_module_prefix():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return ""


class Dot(object):

    def __init__(self):
        self._counter = 0
        self._node_ids = {}

    def start(self):
        print("digraph {")

    def dependency(self, module, dependency):
        print("  {} -> {};".format(
            self._register(module),
            self._register(dependency)
        ))

    def end(self):
        print("}")

    def _register(self, module_name):
        if module_name not in self._node_ids:
            node_id = "id_{}".format(self._counter)
            print("  {} [label=\"{}\"];".format(node_id, module_name))
            self._node_ids[module_name] = node_id
            self._counter += 1
        return self._node_ids[module_name]


if __name__ == "__main__":
    generate_dependency_graph(get_module_prefix())
