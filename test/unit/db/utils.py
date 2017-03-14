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


from timelinelib.test.cases.unit import UnitTestCase
from timelinelib.general.encodings import to_unicode


class describe_raise_error_message_assembly(UnitTestCase):

    def test_can_assemble_bytestrings(self):
        import sys
        specific_msg = u"specific_msg_\xe9"
        cause_exception = "cause_exception"
        path = "foobar"
        err_general = _("Unable to save timeline data to '%s'. File left unmodified.") % path
        err_template = "%s\n\n%%s\n\n%%s" % err_general
        message = err_template % (to_unicode(specific_msg), cause_exception)
        self.assertEqual(u"#Unable to save timeline data to 'foobar'. File left unmodified.#\n\nspecific_msg_\xe9\n\ncause_exception",
                         message)
