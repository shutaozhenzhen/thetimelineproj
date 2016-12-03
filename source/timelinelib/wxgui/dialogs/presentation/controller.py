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


import os
import shutil
import wx
import webbrowser
from timelinelib.wxgui.framework import Controller
from timelinelib.wxgui.utils import get_user_ack
from timelinelib.wxgui.utils import display_error_message
from timelinelib.wxgui.dialogs.presentation.templates import CSS
from timelinelib.wxgui.dialogs.presentation.templates import IMAGE_AND_DESCRIPTION
from timelinelib.wxgui.dialogs.presentation.templates import ONLY_DESCRIPTION
from timelinelib.wxgui.dialogs.presentation.templates import PAGE_TEMPLATE


class PresentationDialogController(Controller):

    def on_init(self, db, canvas):
        self._db = db
        self._canvas = canvas
        self._text_transformer = self._install_text_transformer_plugin()

    def on_change_dir(self, evt):
        self.view.ChangeDir()

    def on_start(self, evt):
        self._pages_dir = self.view.GetTargetDir()
        if len(self._pages_dir.strip()) == 0:
            display_error_message(_("The html pages directory is mandatory"))
            self.view.InvalidTargetDir()
            return
        if not os.path.exists(self._pages_dir):
            query = _("Can't find the html pages directory!" + "\n" + "Do you want to create it?")
            if not get_user_ack(query):
                return
            os.mkdir(self._pages_dir)
        else:
            if len(os.listdir(self._pages_dir)) > 0:
                query = _("The html pages director isn't empty!" + "\n" + "Do you want overwrite it?")
                if not get_user_ack(query):
                    return
        events = self._get_events()
        self._create_images(events)
        self._create_css()
        self._create_pages(events)
        self._display_start_page()
        self.view.EndModalOk()

    def _get_events(self):
        if self.view.AllEventsSelected():
            func = self._get_all_events
        else:
            func = self._get_visible_events
        return sorted([event for event in func() if not event.is_container()], key=lambda event: event.get_start_time())

    def _get_all_events(self):
        return self._db.get_all_events()

    def _get_visible_events(self):
        vp = self._canvas.get_view_properties()
        return vp.filter_events(self._db.get_events(vp.displayed_period))

    def _create_images(self, events):
        shutil.copy(os.path.join("..", "icons", "32.png"), os.path.join(self._pages_dir, "32.png"))
        self._image_source = [""]
        inx = 0
        for event in events:
            inx += 1
            icon = event.get_icon()
            if icon:
                icon.SaveFile(os.path.join(self._pages_dir, "icon_img_%d.bmp" % inx), wx.BITMAP_TYPE_BMP)
                self._image_source.append("icon_img_%d.bmp" % inx)
            else:
                self._image_source.append("")

    def _create_css(self):
        f = open(os.path.join(self._pages_dir, "slideshow.css"), "w")
        f.write(CSS.encode('utf8', 'ignore'))
        f.close()

    def _create_pages(self, events):
        nbr_of_pages = len(events)
        page_nbr = 0
        w1 = events[-1].get_end_time() - events[0].get_start_time()
        pos_style = self._get_positions_style(events)
        pos_history = self.get_position_history(len(events))
        for event in events:
            w2 = event.get_start_time() - events[0].get_start_time()
            p = 2 + int(90 * float(w2.seconds) / float(w1.seconds))
            page_nbr += 1
            next_page_nbr = self._get_next_page_nbr(page_nbr, nbr_of_pages)
            prev_page_nbr = self._get_prev_page_nbr(page_nbr, nbr_of_pages)
            self._create_page(pos_style, p, event, page_nbr, next_page_nbr, prev_page_nbr, pos_history)

    def _get_next_page_nbr(self, page_nbr, nbr_of_pages):
        if page_nbr == nbr_of_pages:
            return 1
        else:
            return page_nbr + 1

    def _get_prev_page_nbr(self, page_nbr, nbr_of_pages):
        if page_nbr == 1:
            return nbr_of_pages
        else:
            return page_nbr - 1

    def _create_page(self, pos_style, p, event, page_nbr, next_page_nbr, prev_page_nbr, pos_history):
        f = open(os.path.join(self._pages_dir, "page_%d.html" % page_nbr), "w")
        if self._image_source[page_nbr] == "":
            x = ONLY_DESCRIPTION % self._text_transformer.transform(event.get_description())
#             pg = PAGE_TEMPLATE2 % (pos_style,
#                                    p,
#                                    self._db.get_time_type().format_period(event.get_time_period()),
#                                    event.get_text(),
#                                    self._text_transformer.transform(event.get_description()),
#                                    prev_page_nbr,
#                                    next_page_nbr,
#                                    pos_history)
        else:
            x = IMAGE_AND_DESCRIPTION % (self._image_source[page_nbr],
                                         self._text_transformer.transform(event.get_description()))

        pg = PAGE_TEMPLATE % (pos_style,
                              p,
                              self._db.get_time_type().format_period(event.get_time_period()),
                              event.get_text(),
                              x,
                              prev_page_nbr,
                              next_page_nbr,
                              pos_history)
        f.write(pg.encode('utf8', 'ignore'))
        f.close()

    def _display_start_page(self):
        webbrowser.open(os.path.join(self._pages_dir, "page_1.html"), new=1)

    def _install_text_transformer_plugin(self):
        from timelinelib.plugin import factory
        from timelinelib.plugin.factory import TEXT_TRANSFORMER
        from timelinelib.plugin.plugins.texttransformers.defaulttexttransformer import DefaultTextTransformer
        plugin = factory.get_plugin(TEXT_TRANSFORMER, "Plain text to HTML transformer") or DefaultTextTransformer()
        return plugin.run()

    def _get_positions_style(self, events):
        template = """div.position_in_history_%d {
    border-radius: 50%%;
    width: 10px;
    height: 10px;
    background-color: #66CDAA;
    position: fixed;
    top: 10px;
    left: %d%%
}
"""
        collector = []
        w1 = events[-1].get_end_time() - events[0].get_start_time()
        nbr = 0
        for event in events:
            nbr += 1
            w2 = event.get_start_time() - events[0].get_start_time()
            p = 2 + int(90 * float(w2.seconds) / float(w1.seconds))
            collector.append(template % (nbr, p))
        return "\n".join(collector)

    def get_position_history(self, count):
        template = '<div class="position_in_history_%d"/>'
        collector = []
        for i in range(count):
            collector.append(template % (i + 1))
        return "\n".join(collector)


def event_key(event):
    return event.get_start_time
