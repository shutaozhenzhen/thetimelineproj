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
import subprocess
import sys

from timelinelib.config.paths import LOCALE_DIR
from timelinelib.test.cases.tmpdir import TmpDirTestCase
from timelinelib.test.cases.unit import UnitTestCase


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


class describe_pot_file(TmpDirTestCase):

    def test_it_is_up_to_date(self):
        checked_in_msgids = get_msgids(os.path.join(LOCALE_DIR, "timeline.pot"))
        generated_msgids = get_msgids(self.generate_pot_file())
        missing_msgids = generated_msgids - checked_in_msgids
        self.assertEqual(missing_msgids, set(), "\n".join([
            "Pot file is not up to date.",
            "Missing msgids:",
        ] + ["- %s" % x for x in missing_msgids] + [
            "Steps to fix:",
            "1. Generate a new pot-file: python tools/generate-pot-file.py",
            "2. Commit it (translations/timeline.pot)",
            "3. Upload it to Launchpad: https://translations.launchpad.net/thetimelineproj/trunk/+translations-upload",
        ]))

    def generate_pot_file(self):
        path = self.get_tmp_path("generated_timeline.pot")
        subprocess.check_output([
            sys.executable,
            os.path.join(os.path.dirname(__file__), "..", "..", "tools", "generate-pot-file.py"),
            "--outfile",
            path
        ], stderr=subprocess.STDOUT)
        return path


def get_po_files():
    for path in os.listdir(LOCALE_DIR):
        if path.endswith(".po"):
            yield os.path.join(LOCALE_DIR, path)


def get_msgids(pot_file):
    msgids = set()
    for (msgid, msgstr) in get_po_entries(pot_file):
        msgids.add(msgid)
    return msgids


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
