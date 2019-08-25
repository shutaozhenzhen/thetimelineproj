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


from timelinelib.wxgui.setup import create_locale_message
from timelinelib.test.cases.unit import UnitTestCase


class testbase(UnitTestCase):
    pass


class localemessage(testbase):

    def test_create_locale_message(self):
        self.assertEqual("Locale setting: %s\nLocale sample date: 3333-11-22" % self.get_locale_info(),
                         create_locale_message())

    def get_locale_info(self):
        import wx
        loc = wx.Locale()
        language_name = loc.GetLanguageName(loc.GetSystemLanguage())
        encoding_name = loc.GetSystemEncodingName()
        return '%s %s' % (language_name, encoding_name)