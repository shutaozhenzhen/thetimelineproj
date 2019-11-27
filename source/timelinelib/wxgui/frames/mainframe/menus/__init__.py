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

# File menu
ID_NEW = wx.ID_NEW
ID_OPEN = wx.ID_OPEN
ID_RECENT = wx.NewId()
ID_SAVEAS = wx.ID_SAVEAS
ID_IMPORT = wx.NewId()
ID_EXPORT = wx.NewId()
ID_EXPORT_ALL = wx.NewId()
ID_EXPORT_SVG = wx.NewId()
ID_EXPORT_LIST = wx.NewId()
ID_EXPORT_FILE = wx.NewId()
ID_EXIT = wx.ID_EXIT

# Edit menu
ID_FIND = wx.ID_FIND
ID_FIND_CATEGORIES = wx.NewId()
ID_FIND_MILESTONES = wx.NewId()
ID_SELECT_ALL = wx.NewId()
ID_PREFERENCES = wx.ID_PREFERENCES
ID_EDIT_SHORTCUTS = wx.NewId()

# View menu
ID_TOOLBAR = wx.NewId()
ID_SIDEBAR = wx.NewId()
ID_LEGEND = wx.NewId()
ID_BALLOONS = wx.NewId()
ID_ZOOMIN = wx.NewId()
ID_ZOOMOUT = wx.NewId()
ID_VERT_ZOOMIN = wx.NewId()
ID_VERT_ZOOMOUT = wx.NewId()
ID_HIDE_DONE = wx.NewId()
ID_PRESENTATION = wx.NewId()
ID_LEFT_ALIGNMENT = wx.NewId()
ID_CENTER_ALIGNMENT = wx.NewId()
ID_EVENTBOX_DRAWER_PLAIN = wx.NewId()
ID_EVENTBOX_DRAWER_GRADIENT_VERTICAL = wx.NewId()
ID_EVENTBOX_DRAWER_GRADIENT_HORIZONTAL = wx.NewId()
ID_EVENTBOX_DRAWER_GRADIENT_HORIZONTAL_ALT = wx.NewId()

# Timeline menu
ID_CREATE_EVENT = wx.NewId()
ID_EDIT_EVENT = wx.NewId()
ID_DUPLICATE_EVENT = wx.NewId()
ID_SET_CATEGORY_ON_SELECTED = wx.NewId()
ID_MOVE_EVENT_UP = wx.NewId()
ID_MOVE_EVENT_DOWN = wx.NewId()
ID_CREATE_MILESTONE = wx.NewId()
ID_COMPRESS = wx.NewId()
ID_MEASURE_DISTANCE = wx.NewId()
ID_SET_CATEGORY_ON_WITHOUT = wx.NewId()
ID_EDIT_ERAS = wx.NewId()
ID_SET_READONLY = wx.NewId()
ID_UNDO = wx.NewId()
ID_REDO = wx.NewId()

# Navigate menu
ID_FIND_FIRST = wx.NewId()
ID_FIND_LAST = wx.NewId()
ID_FIT_ALL = wx.NewId()
ID_RESTORE_TIME_PERIOD = wx.NewId()
ID_NAVIGATE = wx.NewId() + 100

# Help menu
ID_HELP = wx.ID_HELP
ID_TUTORIAL = wx.NewId()
ID_NUMTUTORIAL = wx.NewId()
ID_FEEDBACK = wx.NewId()
ID_CONTACT = wx.NewId()
ID_SYSTEM_INFO = wx.NewId()
ID_ABOUT = wx.ID_ABOUT
