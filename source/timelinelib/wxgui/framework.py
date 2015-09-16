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


import xml.etree.ElementTree

import wx


class GuiCreator(object):

    def _create(self, controller_class, variables):
        self._variables = variables
        self.controller = controller_class(self)
        return self._create_from_node(self, xml.etree.ElementTree.fromstring(self.__doc__))

    def _create_from_node(self, parent, node):
        try:
            creator = getattr(self, "_create_%s" % node.tag)
        except AttributeError:
            creator = self._create_generic_component
        component = creator(parent, node)
        self._bind_events(node, component)
        if node.get("id", None):
            setattr(self, node.get("id"), component)
        return component

    def _create_StdDialogButtonSizer(self, parent, node):
        return self.CreateStdDialogButtonSizer(flags=self._get_or_value(node.get("buttons", "")))

    def _create_BoxSizerVertical(self, parent, node):
        return self._populate_sizer(parent, node, wx.BoxSizer(wx.VERTICAL))

    def _create_BoxSizerHorizontal(self, parent, node):
        return self._populate_sizer(parent, node, wx.BoxSizer(wx.HORIZONTAL))

    def _create_StaticBoxSizerVertical(self, parent, node):
        box = wx.StaticBox(parent, label=self._get_text(node.get("label", "")), **self._get_wx_window_attributes(node))
        return self._populate_sizer(parent, node, wx.StaticBoxSizer(box, wx.HORIZONTAL))

    def _populate_sizer(self, parent, node, sizer):
        for child_node in node.getchildren():
            if child_node.tag == "Spacer":
                sizer.AddSpacer(int(child_node.get("size", "5")))
            else:
                component = self._create_from_node(parent, child_node)
                border = self._get_or_value(child_node.get("border", ""))
                sizer.Add(component,
                          flag=border|wx.EXPAND,
                          border=12,
                          proportion=int(child_node.get("proportion", "0")))
        return sizer

    def _create_generic_component(self, parent, node):
        component = getattr(wx, node.tag)(parent, **self._get_wx_window_attributes(node))
        for child_node in node.getchildren():
            self._create_from_node(component, child_node)
        return component

    def _get_text(self, text):
        if text.startswith("$(") and text.endswith(")"):
            return self._variables[text[2:-1]]
        else:
            return text

    def _get_wx_window_attributes(self, node):
        return {
            "size": (int(node.get("width", "-1")),
                     int(node.get("height", "-1"))),
            "style": self._get_or_value(node.get("style", None))
        }

    def _get_or_value(self, wx_constant_names):
        value = 0
        if wx_constant_names:
            for wx_constant_name in wx_constant_names.split("|"):
                value |= getattr(wx, wx_constant_name)
        return value

    def _bind_events(self, node, component):
        for key in node.keys():
            if key.startswith("event_"):
                event_name = key[6:]
                target = getattr(self.controller, node.get(key))
                self.Bind(getattr(wx, event_name), target, component)


class Dialog(wx.Dialog, GuiCreator):

    def __init__(self, controller_class, parent, variables={}, **kwargs):
        wx.Dialog.__init__(self, parent, **kwargs)
        component = self._create(controller_class, variables)
        if isinstance(component, wx.Sizer):
            self.SetSizerAndFit(component)


class Controller(object):

    def __init__(self, view):
        self.view = view
