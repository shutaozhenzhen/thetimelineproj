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


from timelinelib.plugin.pluginbase import PluginBase
from timelinelib.plugin.plugins.eventboxdrawers import EVENTBOX_DRAWER
import timelinelib.wxgui.frames.mainframe.menus as mid


class OtherGradientEventBoxDrawer(PluginBase):

    def service(self):
        return EVENTBOX_DRAWER

    def display_name(self):
        return _("Other Gradient Event box drawer")

    @staticmethod
    def wxid():
        return mid.ID_EVENTBOX_DRAWER_GRADIENT_HORIZONTAL

    def run(self):
        from timelinelib.canvas.eventboxdrawers.othergradienteventboxdrawer import OtherGradientEventBoxDrawer
        return OtherGradientEventBoxDrawer()
