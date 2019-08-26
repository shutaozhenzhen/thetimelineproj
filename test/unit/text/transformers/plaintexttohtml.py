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


from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.text.transformers.plaintexttohtml import PlainTextToHtml


class describe_plain_text_to_html_transformer(UnitTestCase):

    def test_simple_text_is_returned_asis(self):
        self.assertEqual("", self.transformer.transform(""))

    def test_none_text_is_returned_as_empty_string(self):
        self.assertEqual("", self.transformer.transform(None))

    def test_newline_chars_are_converted_to_breaks(self):
        self.assertEqual("", self.transformer.transform("\n"))

    def test_lt_and_gt_are_converted_html_codes(self):
        self.assertEqual("<p>&lt;&gt;</p>", self.transformer.transform("<>"))

    def test_lt_and_gt_preserved_for_br(self):
        self.assertEqual("<blockquote>\n<p>&lt;</p>\n</blockquote>", self.transformer.transform(">\n<"))

    def setUp(self):
        self.transformer = PlainTextToHtml()
