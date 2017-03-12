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

"""
Unittest of class :doc:`DefaultTextTransformer
<timelinelib_text_transformers_defaulttransformer>`
"""

from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.text.transformers.defaulttransformer import DefaultTextTransformer


class describe_default_text_transformer(UnitTestCase):
    """ """

    def test_simple_text_is_retruned_asis(self):
        """ """
        self.assertEqual("", self.transformer.transform(""))

    def test_none_text_is_retruned_as_empty_string(self):
        """ """
        self.assertEqual("", self.transformer.transform(None))

    def setUp(self):
        """ """
        self.transformer = DefaultTextTransformer()
