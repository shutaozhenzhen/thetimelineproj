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


import codecs
import os

from timelinelib.test.cases.unit import UnitTestCase
import timelinelib.meta.about
import timelinelib.meta.version as version


class SourceCodeDistributionSpec(UnitTestCase):

    def test_version_number_in_changelog_should_match_that_in_version_module(self):
        self.assertTrue(
            version.get_version_number_string() in
            self.read_first_version_line_from(self.changelog))

    def test_all_authors_mentioned_in_about_module_should_be_mentioned_in_AUTHORS(self):
        authors_content = self.read_utf8_encoded_text_from(self.AUTHORS)
        for author in self.get_authors_from_about_module():
            self.assertTrue(author in authors_content)

    def test_py_files_should_have_copyright(self):
        for py_file in self.get_py_files(["source", "test", "tools"]):
            with open(py_file) as f:
                content = f.read()
                if content:
                    self.assertIn(COPYRIGHT_HEADER, content, "%s lacks proper copyright notice." % py_file)

    def test_unit_tests_have_corresponding_module(self):
        unit_test_dir = os.path.join("test", "unit")
        for unit_file in self.get_py_files([unit_test_dir]):
            module_file = os.path.relpath(os.path.join(
                self.ROOT_DIR,
                "source",
                "timelinelib",
                os.path.relpath(unit_file, os.path.join(self.ROOT_DIR, unit_test_dir))
            ))
            self.assertTrue(
                os.path.exists(module_file),
                "Found unit test '%s', but not module '%s'" % (unit_file, module_file)
            )

    def setUp(self):
        self.ROOT_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
        self.README = os.path.join(self.ROOT_DIR, "README")
        self.changelog = os.path.join(self.ROOT_DIR, "documentation", "changelog.rst")
        self.AUTHORS = os.path.join(self.ROOT_DIR, "AUTHORS")

    def get_py_files(self, subdirs):
        for subdir in subdirs:
            for (root, dirs, files) in os.walk(os.path.join(self.ROOT_DIR, subdir)):
                for file in files:
                    if file.endswith(".py"):
                        yield os.path.relpath(os.path.normpath(os.path.join(root, file)))

    def get_authors_from_about_module(self):
        return [possible_author.strip()
                for possible_author
                in self.get_possible_authors_from_about_module()
                if self.is_author_from_about_module(possible_author)]

    def get_possible_authors_from_about_module(self):
        return (timelinelib.meta.about.DEVELOPERS +
                timelinelib.meta.about.TRANSLATORS +
                timelinelib.meta.about.ARTISTS)

    def is_author_from_about_module(self, possible_author):
        return possible_author and not self.is_header(possible_author)

    def is_header(self, possible_author):
        return ":" in possible_author

    def read_first_version_line_from(self, path):
        f = open(path, "r")
        while True:
            first_version_line = f.readline()
            if first_version_line.startswith("Version"):
                break
        f.close()
        return first_version_line

    def read_utf8_encoded_text_from(self, path):
        f = codecs.open(path, "r", "utf-8")
        content = f.read()
        f.close()
        return content


COPYRIGHT_HEADER = "".join([
    "# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017  Rickard Lindberg, Roger Lindberg\n",
    "#\n",
    "# This file is part of Timeline.\n",
    "#\n",
    "# Timeline is free software: you can redistribute it and/or modify\n",
    "# it under the terms of the GNU General Public License as published by\n",
    "# the Free Software Foundation, either version 3 of the License, or\n",
    "# (at your option) any later version.\n",
    "#\n",
    "# Timeline is distributed in the hope that it will be useful,\n",
    "# but WITHOUT ANY WARRANTY; without even the implied warranty of\n",
    "# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n",
    "# GNU General Public License for more details.\n",
    "#\n",
    "# You should have received a copy of the GNU General Public License\n",
    "# along with Timeline.  If not, see <http://www.gnu.org/licenses/>.\n",
])
