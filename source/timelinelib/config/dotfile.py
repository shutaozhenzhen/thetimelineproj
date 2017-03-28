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


"""
Handle application configuration.

This module is global and can be used by all modules. Before accessing
configurations, the read function should be called. To save the current
configuration back to file, call the write method.
"""


from ConfigParser import ConfigParser
from ConfigParser import DEFAULTSECT
import os.path
import sys

import wx

from timelinelib.calendar.gregorian.dateformatter import GregorianDateFormatter
from timelinelib.config.dateformatparser import DateFormatParser
from timelinelib.general.observer import Observable
from timelinelib.wxgui.components.font import Font
from timelinelib.wxgui.utils import display_information_message


# Name used in ConfigParser
SELECTED_EVENT_BOX_DRAWER = "selected_event_box_drawer"
WINDOW_WIDTH = "window_width"
WINDOW_HEIGHT = "window_height"
WINDOW_XPOS = "window xpos"
WINDOW_YPOS = "window ypos"
WINDOW_MAXIMIZED = "window_maximized"
SHOW_TOOLBAR = "show_toolbar"
SHOW_SIDEBAR = "show_sidebar"
SHOW_LEGEND = "show_legend"
SIDEBAR_WIDTH = "sidebar_width"
RECENT_FILES = "recent_files"
OPEN_RECENT_AT_STARTUP = "open_recent_at_startup"
BALLOON_ON_HOVER = "balloon_on_hover"
HIDE_EVENTS_DONE = "hide_events_done"
WEEK_START = "week_start"
USE_INERTIAL_SCROLLING = "use_inertial_scrolling"
EXPERIMENTAL_FEATURES = "experimental_features"
DIVIDER_LINE_SLIDER_POS = "divider_line_slider_pos"
NEVER_SHOW_PERIOD_EVENTS_AS_POINT_EVENTS = "never_show_period_events_as_point_events"
DRAW_POINT_EVENTS_TO_RIGHT = "draw_point_events_to_right"
MAJOR_STRIP_FONT = "major_strip_font"
MINOR_STRIP_FONT = "minor_strip_font"
LEGEND_FONT = "legend_font"
EVENT_EDITOR_SHOW_PERIOD = "event_editor_show_period"
EVENT_EDITOR_SHOW_TIME = "event_editor_show_time"
EVENT_EDITOR_TAB_ORDER = "event_editor_tab_order"
CENTER_EVENT_TEXTS = "center_event_texts"
UNCHECK_TIME_FOR_NEW_EVENTS = "uncheck_time_for_new_events"
MINOR_STRIP_DIVIDER_LINE_COLOUR = "minor_strip_divider_line_colour"
MAJOR_STRIP_DIVIDER_LINE_COLOUR = "major_strip_divider_line_colour"
NOW_LINE_COLOUR = "today_line_colour"
WEEKEND_COLOUR = "weekend_colour"
BG_COLOUR = "bg_colour"
TEXT_BELOW_ICON = "text_below_icon"
FUZZY_ICON = "fuzzy_icon"
LOCKED_ICON = "locked_icon"
HYPERLINK_ICON = "hyperlink_icon"
DATE_FORMAT = "date_format"
VERTCAL_SPACE_BETWEEN_EVENTS = "vertical_space_between_events"
COLORIZE_WEEKENDS = "colorize_weekens"
SKIP_S_IN_DECADE_TEXT = "skip_s_in_decade_text"
DISPLAY_CHECKMARK_ON_EVENTS_DONE = "display_checkmark_on_events-done"
NEVER_USE_TIME = "never_use_time"
LEGEND_POS = "legend_pos"
DEFAULTS = {
    SELECTED_EVENT_BOX_DRAWER: "Default Event box drawer",
    WINDOW_WIDTH: "900",
    WINDOW_HEIGHT: "500",
    WINDOW_XPOS: "-1",
    WINDOW_YPOS: "-1",
    WINDOW_MAXIMIZED: "False",
    SHOW_TOOLBAR: "True",
    SHOW_SIDEBAR: "True",
    SIDEBAR_WIDTH: "200",
    SHOW_LEGEND: "True",
    OPEN_RECENT_AT_STARTUP: "True",
    RECENT_FILES: "",
    BALLOON_ON_HOVER: "True",
    WEEK_START: "monday",
    USE_INERTIAL_SCROLLING: "False",
    EXPERIMENTAL_FEATURES: "",
    DIVIDER_LINE_SLIDER_POS: "50",
    NEVER_SHOW_PERIOD_EVENTS_AS_POINT_EVENTS: "False",
    DRAW_POINT_EVENTS_TO_RIGHT: "False",
    EVENT_EDITOR_SHOW_PERIOD: "False",
    EVENT_EDITOR_SHOW_TIME: "False",
    EVENT_EDITOR_TAB_ORDER: "01234:",
    CENTER_EVENT_TEXTS: "False",
    UNCHECK_TIME_FOR_NEW_EVENTS: "False",
    MINOR_STRIP_DIVIDER_LINE_COLOUR: "(200, 200, 200)",
    MAJOR_STRIP_DIVIDER_LINE_COLOUR: "(200, 200, 200)",
    NOW_LINE_COLOUR: "(200, 0, 0)",
    WEEKEND_COLOUR: "(255, 255, 255)",
    BG_COLOUR: "(255, 255, 255)",
    TEXT_BELOW_ICON: "False",
    FUZZY_ICON: "fuzzy.png",
    LOCKED_ICON: "locked.png",
    HYPERLINK_ICON: "hyperlink.png",
    DATE_FORMAT: "yyyy-mm-dd",
    VERTCAL_SPACE_BETWEEN_EVENTS: "5",
    COLORIZE_WEEKENDS: "False",
    SKIP_S_IN_DECADE_TEXT: "False",
    DISPLAY_CHECKMARK_ON_EVENTS_DONE: "False",
    NEVER_USE_TIME: "False",
    LEGEND_POS: "0"
}
# Some settings
MAX_NBR_OF_RECENT_FILES_SAVED = 5
ENCODING = "utf-8"


def read_config(path):
    config = Config(path)
    config.read()
    return config


class Config(Observable):
    """
    Provide read and write access to application configuration settings.

    Built as a wrapper around ConfigParser: Properties exist to read and write
    values but ConfigParser does the actual reading and writing of the
    configuration file.
    """

    def __init__(self, path):
        Observable.__init__(self)
        self.path = path
        self._set_default_fonts()
        self.config_parser = ConfigParser(DEFAULTS)

    def read(self):
        """Read settings from file specified in constructor."""
        self.config_parser.read(self.path)

    def write(self):
        """
        Write settings to file specified in constructor and raise IOError if
        failed.
        """
        f = open(self.path, "w")
        try:
            self.config_parser.write(f)
        finally:
            f.close()

    def get_selected_event_box_drawer(self):
        return self.config_parser.get(DEFAULTSECT, SELECTED_EVENT_BOX_DRAWER).decode("utf-8")

    def set_selected_event_box_drawer(self, selected):
        self.config_parser.set(DEFAULTSECT, SELECTED_EVENT_BOX_DRAWER, str(selected.encode("utf-8")))

    def get_window_size(self):
        return (self.config_parser.getint(DEFAULTSECT, WINDOW_WIDTH),
                self.config_parser.getint(DEFAULTSECT, WINDOW_HEIGHT))

    def set_window_size(self, size):
        width, height = size
        self.config_parser.set(DEFAULTSECT, WINDOW_WIDTH, str(width))
        self.config_parser.set(DEFAULTSECT, WINDOW_HEIGHT, str(height))

    def get_window_pos(self):
        width, _ = self.get_window_size()
        # Make sure that some area of the window is visible on the screen
        # Some part of the titlebar must be visible
        xpos = max(-width + 100,
                   self.config_parser.getint(DEFAULTSECT, WINDOW_XPOS))
        # Titlebar must not be above the upper screen border
        ypos = max(0, self.config_parser.getint(DEFAULTSECT, WINDOW_YPOS))
        return (xpos, ypos)

    def set_window_pos(self, pos):
        xpos, ypos = pos
        self.config_parser.set(DEFAULTSECT, WINDOW_XPOS, str(xpos))
        self.config_parser.set(DEFAULTSECT, WINDOW_YPOS, str(ypos))

    def get_window_maximized(self):
        return self.config_parser.getboolean(DEFAULTSECT, WINDOW_MAXIMIZED)

    def set_window_maximized(self, maximized):
        self.config_parser.set(DEFAULTSECT, WINDOW_MAXIMIZED, str(maximized))

    def get_show_toolbar(self):
        return self.config_parser.getboolean(DEFAULTSECT, SHOW_TOOLBAR)

    def set_show_toolbar(self, show):
        self.config_parser.set(DEFAULTSECT, SHOW_TOOLBAR, str(show))
        self._notify()

    def get_show_sidebar(self):
        return self.config_parser.getboolean(DEFAULTSECT, SHOW_SIDEBAR)

    def set_show_sidebar(self, show):
        self.config_parser.set(DEFAULTSECT, SHOW_SIDEBAR, str(show))

    def get_show_legend(self):
        return self.config_parser.getboolean(DEFAULTSECT, SHOW_LEGEND)

    def set_show_legend(self, show):
        self.config_parser.set(DEFAULTSECT, SHOW_LEGEND, str(show))
        self._notify()

    def get_never_use_time(self):
        return self.config_parser.getboolean(DEFAULTSECT, NEVER_USE_TIME)

    def set_never_use_time(self, value):
        self.config_parser.set(DEFAULTSECT, NEVER_USE_TIME, str(value))
        self._notify()

    def get_sidebar_width(self):
        return self.config_parser.getint(DEFAULTSECT, SIDEBAR_WIDTH)

    def set_sidebar_width(self, width):
        self.config_parser.set(DEFAULTSECT, SIDEBAR_WIDTH, str(width))

    def get_divider_line_slider_pos(self):
        return self.config_parser.getint(DEFAULTSECT, DIVIDER_LINE_SLIDER_POS)

    def set_divider_line_slider_pos(self, pos):
        self.config_parser.set(DEFAULTSECT, DIVIDER_LINE_SLIDER_POS, str(pos))

    def get_recently_opened(self):
        ro = self.config_parser.get(DEFAULTSECT, RECENT_FILES).decode(ENCODING).split(",")
        # Filter out empty elements: "".split(",") will return [""] but we want
        # the empty list
        ro_filtered = [x for x in ro if x]
        return ro_filtered

    def has_recently_opened_files(self):
        if not self.get_open_recent_at_startup():
            return False
        else:
            return len(self.get_recently_opened()) > 0

    def get_latest_recently_opened_file(self):
        return self.get_recently_opened()[0]

    def append_recently_opened(self, path):
        if path in [":tutorial:"]:
            # Special timelines should not be saved
            return
        if isinstance(path, str):
            # This path might have come from the command line so we need to convert
            # it to unicode
            path = path.decode(sys.getfilesystemencoding())
        abs_path = os.path.abspath(path)
        current = self.get_recently_opened()
        # Just keep one entry of the same path in the list
        if abs_path in current:
            current.remove(abs_path)
        current.insert(0, abs_path)
        self.config_parser.set(DEFAULTSECT, RECENT_FILES,
                               (",".join(current[:MAX_NBR_OF_RECENT_FILES_SAVED])).encode(ENCODING))

    def get_open_recent_at_startup(self):
        return self.config_parser.getboolean(DEFAULTSECT, OPEN_RECENT_AT_STARTUP)

    def set_open_recent_at_startup(self, value):
        self.config_parser.set(DEFAULTSECT, OPEN_RECENT_AT_STARTUP, str(value))

    def get_balloon_on_hover(self):
        return self.config_parser.getboolean(DEFAULTSECT, BALLOON_ON_HOVER)

    def set_balloon_on_hover(self, balloon_on_hover):
        self.config_parser.set(DEFAULTSECT, BALLOON_ON_HOVER, str(balloon_on_hover))
        self._notify()

    @property
    def hide_events_done(self):
        return self.config_parser.getboolean(DEFAULTSECT, HIDE_EVENTS_DONE)

    @hide_events_done.setter
    def hide_events_done(self, value):
        self.config_parser.set(DEFAULTSECT, HIDE_EVENTS_DONE, str(value))
        self._notify()

    def get_uncheck_time_for_new_events(self):
        return self.config_parser.getboolean(DEFAULTSECT, UNCHECK_TIME_FOR_NEW_EVENTS)

    def set_uncheck_time_for_new_events(self, value):
        self.config_parser.set(DEFAULTSECT, UNCHECK_TIME_FOR_NEW_EVENTS, str(value))

    def get_week_start(self):
        return self.config_parser.get(DEFAULTSECT, WEEK_START)

    def set_week_start(self, week_start):
        if week_start not in ["monday", "sunday"]:
            raise ValueError("Invalid week start.")
        self.config_parser.set(DEFAULTSECT, WEEK_START, week_start)
        self._notify()

    def get_use_inertial_scrolling(self):
        return self.config_parser.getboolean(DEFAULTSECT, USE_INERTIAL_SCROLLING)

    def set_use_inertial_scrolling(self, value):
        self.config_parser.set(DEFAULTSECT, USE_INERTIAL_SCROLLING, str(value))
        self._notify()

    def get_shortcut_key(self, cfgid, default):
        try:
            return self.config_parser.get(DEFAULTSECT, cfgid)
        except:
            self.set_shortcut_key(cfgid, default)
            return default

    def set_shortcut_key(self, cfgid, value):
        self.config_parser.set(DEFAULTSECT, cfgid, value)

    def get_experimental_features(self):
        return self.config_parser.get(DEFAULTSECT, EXPERIMENTAL_FEATURES)

    def set_experimental_features(self, value):
        self.config_parser.set(DEFAULTSECT, EXPERIMENTAL_FEATURES, value)
        self._notify()

    def get_never_show_period_events_as_point_events(self):
        return self.config_parser.getboolean(DEFAULTSECT, NEVER_SHOW_PERIOD_EVENTS_AS_POINT_EVENTS)

    def set_never_show_period_events_as_point_events(self, value):
        self.config_parser.set(DEFAULTSECT, NEVER_SHOW_PERIOD_EVENTS_AS_POINT_EVENTS, str(value))
        self._notify()

    def get_center_event_texts(self):
        return self.config_parser.getboolean(DEFAULTSECT, CENTER_EVENT_TEXTS)

    def set_center_event_texts(self, value):
        self.config_parser.set(DEFAULTSECT, CENTER_EVENT_TEXTS, str(value))
        self._notify()

    def get_draw_period_events_to_right(self):
        return self.config_parser.getboolean(DEFAULTSECT, DRAW_POINT_EVENTS_TO_RIGHT)

    def set_draw_period_events_to_right(self, value):
        self.config_parser.set(DEFAULTSECT, DRAW_POINT_EVENTS_TO_RIGHT, str(value))
        self._notify()

    def get_major_strip_font(self):
        return self.config_parser.get(DEFAULTSECT, MAJOR_STRIP_FONT)

    def set_major_strip_font(self, font):
        if self._toStr(font) is not None:
            self.config_parser.set(DEFAULTSECT, MAJOR_STRIP_FONT, font)
            self._notify()

    def get_minor_strip_font(self):
        return self.config_parser.get(DEFAULTSECT, MINOR_STRIP_FONT)

    def set_minor_strip_font(self, font):
        if self._toStr(font) is not None:
            self.config_parser.set(DEFAULTSECT, MINOR_STRIP_FONT, font)
            self._notify()

    def get_legend_font(self):
        return self.config_parser.get(DEFAULTSECT, LEGEND_FONT)

    def set_legend_font(self, font):
        if self._toStr(font) is not None:
            self.config_parser.set(DEFAULTSECT, LEGEND_FONT, font)
            self._notify()

    def _set_default_fonts(self):
        DEFAULTS[MAJOR_STRIP_FONT] = Font(12, weight=wx.FONTWEIGHT_BOLD).serialize()
        DEFAULTS[MINOR_STRIP_FONT] = Font(8).serialize()
        DEFAULTS[LEGEND_FONT] = Font(8).serialize()

    def get_event_editor_show_period(self):
        return self.config_parser.getboolean(DEFAULTSECT, EVENT_EDITOR_SHOW_PERIOD)

    def set_event_editor_show_period(self, value):
        self.config_parser.set(DEFAULTSECT, EVENT_EDITOR_SHOW_PERIOD, str(value))
    event_editor_show_period = property(get_event_editor_show_period, set_event_editor_show_period)

    def get_event_editor_show_time(self):
        return self.config_parser.getboolean(DEFAULTSECT, EVENT_EDITOR_SHOW_TIME)

    def set_event_editor_show_time(self, value):
        self.config_parser.set(DEFAULTSECT, EVENT_EDITOR_SHOW_TIME, str(value))
    event_editor_show_time = property(get_event_editor_show_time, set_event_editor_show_time)

    def get_event_editor_tab_order(self):
        return self.config_parser.get(DEFAULTSECT, EVENT_EDITOR_TAB_ORDER)

    def set_event_editor_tab_order(self, tab_order):
        self.config_parser.set(DEFAULTSECT, EVENT_EDITOR_TAB_ORDER, tab_order)
    event_editor_tab_order = property(get_event_editor_tab_order, set_event_editor_tab_order)

    def get_minor_strip_divider_line_colour(self):
        return self._string_to_tuple(self.config_parser.get(DEFAULTSECT, MINOR_STRIP_DIVIDER_LINE_COLOUR))

    def set_minor_strip_divider_line_colour(self, colour):
        self.config_parser.set(DEFAULTSECT, MINOR_STRIP_DIVIDER_LINE_COLOUR, self._tuple_to_string(colour))
        self._notify()
    minor_strip_divider_line_colour = property(get_minor_strip_divider_line_colour, set_minor_strip_divider_line_colour)

    def get_major_strip_divider_line_colour(self):
        return self._string_to_tuple(self.config_parser.get(DEFAULTSECT, MAJOR_STRIP_DIVIDER_LINE_COLOUR))

    def set_major_strip_divider_line_colour(self, colour):
        self.config_parser.set(DEFAULTSECT, MAJOR_STRIP_DIVIDER_LINE_COLOUR, self._tuple_to_string(colour))
        self._notify()
    major_strip_divider_line_colour = property(get_major_strip_divider_line_colour, set_major_strip_divider_line_colour)

    def get_now_line_color(self):
        return self._string_to_tuple(self.config_parser.get(DEFAULTSECT, NOW_LINE_COLOUR))

    def set_now_line_color(self, colour):
        self.config_parser.set(DEFAULTSECT, NOW_LINE_COLOUR, self._tuple_to_string(colour))
        self._notify()
    now_line_colour = property(get_now_line_color, set_now_line_color)

    def get_weekend_color(self):
        return self._string_to_tuple(self.config_parser.get(DEFAULTSECT, WEEKEND_COLOUR))

    def set_weekend_color(self, colour):
        self.config_parser.set(DEFAULTSECT, WEEKEND_COLOUR, self._tuple_to_string(colour))
        self._notify()
    weekend_colour = property(get_weekend_color, set_weekend_color)

    def get_bg_color(self):
        return self._string_to_tuple(self.config_parser.get(DEFAULTSECT, BG_COLOUR))

    def set_bg_color(self, colour):
        self.config_parser.set(DEFAULTSECT, BG_COLOUR, self._tuple_to_string(colour))
        self._notify()

    def get_text_below_icon(self):
        return self.config_parser.getboolean(DEFAULTSECT, TEXT_BELOW_ICON)

    def set_text_below_icon(self, value):
        self.config_parser.set(DEFAULTSECT, TEXT_BELOW_ICON, str(value))
        self._notify()
    text_below_icon = property(get_text_below_icon, set_text_below_icon)

    def _string_to_tuple(self, tuple_string):
        return tuple([int(x.strip()) for x in tuple_string[1:-1].split(",")])

    def _tuple_to_string(self, tuple_data):
        return str(tuple_data)

    def get_fuzzy_icon(self):
        return self.config_parser.get(DEFAULTSECT, FUZZY_ICON)

    def set_fuzzy_icon(self, value):
        self.config_parser.set(DEFAULTSECT, FUZZY_ICON, value)
        self._notify()

    @property
    def legend_pos(self):
        return self.config_parser.getint(DEFAULTSECT, LEGEND_POS)

    @legend_pos.setter
    def legend_pos(self, pos):
        self.config_parser.set(DEFAULTSECT, LEGEND_POS, str(min(3, max(0, pos))))
        self._notify()

    def get_locked_icon(self):
        return self.config_parser.get(DEFAULTSECT, LOCKED_ICON)

    def set_locked_icon(self, value):
        self.config_parser.set(DEFAULTSECT, LOCKED_ICON, value)
        self._notify()

    def get_hyperlink_icon(self):
        return self.config_parser.get(DEFAULTSECT, HYPERLINK_ICON)

    def set_hyperlink_icon(self, value):
        self.config_parser.set(DEFAULTSECT, HYPERLINK_ICON, value)
        self._notify()

    def get_date_formatter(self):
        parser = DateFormatParser().parse(self.get_date_format())
        date_formatter = GregorianDateFormatter()
        date_formatter.set_separators(*parser.get_separators())
        date_formatter.set_region_order(*parser.get_region_order())
        date_formatter.use_abbreviated_name_for_month(parser.use_abbreviated_month_names())
        return date_formatter

    def get_date_format(self):
        return self.config_parser.get(DEFAULTSECT, DATE_FORMAT)

    def set_date_format(self, date_format):
        self.config_parser.set(DEFAULTSECT, DATE_FORMAT, date_format)
        self._notify()
    date_format = property(get_date_format, set_date_format)

    def get_vertical_space_between_events(self):
        return self.config_parser.getint(DEFAULTSECT, VERTCAL_SPACE_BETWEEN_EVENTS)

    def set_vertical_space_between_events(self, value):
        self.config_parser.set(DEFAULTSECT, VERTCAL_SPACE_BETWEEN_EVENTS, str(max(0, value)))
        self._notify()

    def get_colorize_weekends(self):
        return self.config_parser.getboolean(DEFAULTSECT, COLORIZE_WEEKENDS)

    def set_colorize_weekends(self, value):
        self.config_parser.set(DEFAULTSECT, COLORIZE_WEEKENDS, str(value))
        self._notify()

    def get_skip_s_in_decade_text(self):
        return self.config_parser.getboolean(DEFAULTSECT, SKIP_S_IN_DECADE_TEXT)

    def set_skip_s_in_decade_text(self, value):
        self.config_parser.set(DEFAULTSECT, SKIP_S_IN_DECADE_TEXT, str(value))
        self._notify()

    def get_display_checkmark_on_events_done(self):
        return self.config_parser.getboolean(DEFAULTSECT, DISPLAY_CHECKMARK_ON_EVENTS_DONE)

    def set_display_checkmark_on_events_done(self, value):
        self.config_parser.set(DEFAULTSECT, DISPLAY_CHECKMARK_ON_EVENTS_DONE, str(value))
        self._notify()

    def _toStr(self, value):
        try:
            return str(value)
        except UnicodeEncodeError:
            display_information_message(_("Warning"), _("The selected value contains invalid characters and can't be saved"))
