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


import wx
from wx._gdi_ import DC_MinX


LABEL = _("In: ")
NAME = _("Select period")

class PeriodSelection:
    
    def __init__(self, parent, controller):
        self._controller = controller
        choices = []
        self._period_label = wx.StaticText(parent, wx.ID_ANY, LABEL) 
        parent.AddControl(self._period_label)
        self._period = wx.Choice(parent, wx.ID_ANY, size=(150, -1), choices=choices, name=NAME)
        parent.Bind(wx.EVT_CHOICE, self._event_handler, self._period)
        parent.AddControl(self._period)
        self._period.SetSelection(0)

    def SetPeriodSelections(self, values):
        if values:
            self.Clear()
            for value in values:
                self._period.Append(value)
            self.SetSelection(0)
            self.Show(True)
        else:
            self.Show(False)
                            
    def Clear(self):
        self._period.Clear()
        
    def Show(self, value):
        self._period.Show(value)
        self._period_label.Show(value)
        
    def SetSelection(self, inx):
        self._period.SetSelection(inx)
        
    def GetString(self):
        return self._period.GetString(self._period.GetSelection())        
                        
    def _event_handler(self, evt):
        pass