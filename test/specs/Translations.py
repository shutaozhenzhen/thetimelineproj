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

from timelinelib.config.paths import LOCALE_DIR
from timelinetest import UnitTestCase


class describe_po_files(UnitTestCase):

    def test_message_strings_have_correct_number_of_placeholders(self):
        for po_file in get_po_files():
            for (msgid, msgstr) in get_po_entries(po_file):
                if len(msgstr) > 0:
                    self.assertEqual(
                        msgid.count("%s"),
                        msgstr.count("%s"),
                        "Po file '%s' is missing placeholder for msgid '%s'" % (
                            os.path.basename(po_file),
                            msgid
                        )
                    )


def get_po_files():
    for path in os.listdir(LOCALE_DIR):
        if path.endswith(".po"):
            yield os.path.join(LOCALE_DIR, path)


def get_po_entries(path):
    with open(path) as f:
        return parse_po_entries(f.readlines())


def parse_po_entries(lines):
    msgid = None
    msgstr = None
    while len(lines) > 0:
        line = lines.pop(0)
        if line.startswith("msgid"):
            lines.insert(0, line[6:])
            msgid = parse_string(lines)
        if line.startswith("msgstr"):
            lines.insert(0, line[7:])
            msgstr = parse_string(lines)
            yield (msgid, msgstr)


def parse_string(lines):
    string = ""
    while (len(lines) > 0 and
           lines[0].startswith("\"") and
           lines[0].rstrip().endswith("\"")):
        string += lines.pop(0).rstrip()[1:-1]
    return string.decode("string-escape").decode("utf-8")
