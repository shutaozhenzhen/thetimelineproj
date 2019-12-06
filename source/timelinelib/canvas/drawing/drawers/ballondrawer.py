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


import math
import os

import wx

from timelinelib.config.paths import ICONS_DIR


BALLOON_RADIUS = 12
ARROW_OFFSET = BALLOON_RADIUS + 25
MIN_TEXT_WIDTH = 200
SLIDER_WIDTH = 20


class BallonDrawer:

    def __init__(self, dc):
        self._dc = dc

    @staticmethod
    def get_icon_size(event):
        (iw, ih) = (0, 0)
        icon = event.get_data("icon")
        if icon is not None:
            (iw, ih) = icon.Size
        return iw, ih

    @staticmethod
    def max_text_width(scene, event_rect, icon_width):
        padding = 2 * BALLOON_RADIUS
        if icon_width > 0:
            padding += BALLOON_RADIUS
        else:
            icon_width = 0
        padding += icon_width
        visble_background = scene.width - SLIDER_WIDTH
        balloon_width = visble_background - event_rect.X - event_rect.width // 2 + ARROW_OFFSET
        max_text_width = balloon_width - padding
        return max(MIN_TEXT_WIDTH, max_text_width)

    def get_description_lines(self, event, max_text_width, iw):
        description = event.get_data("description")
        if description is not None:
            return break_text(description, self._dc, max_text_width)

    def draw_balloon_bg(self, inner_size, tip_pos, above, sticky):
        """
        Draw the balloon background leaving inner_size for content.

        tip_pos determines where the tip of the ballon should be.

        above determines if the balloon should be above the tip (True) or below
        (False). This is not currently implemented.

                    W
           |----------------|
             ______________           _
            /              \          |             R = Corner Radius
           |                |         |            AA = Left Arrow-leg angle
           |  W_ARROW       |         |  H     MARGIN = Text margin
           |     |--|       |         |             * = Starting point
            \____    ______/          _
                /  /                  |
               /_/                    |  H_ARROW
              *                       -
           |----|
           ARROW_OFFSET

        Calculation of points starts at the tip of the arrow and continues
        clockwise around the ballon.

        Return (bounding_rect, x, y) where x and y is at top of inner region.
        """
        # Prepare path object
        gc = wx.GraphicsContext.Create(self._dc)
        path = gc.CreatePath()
        # Calculate path
        R = BALLOON_RADIUS
        W = 1 * R + inner_size[0]
        H = 1 * R + inner_size[1]
        H_ARROW = 14
        W_ARROW = 15
        AA = 20
        # Starting point at the tip of the arrow
        (tipx, tipy) = tip_pos
        p0 = wx.Point(tipx, tipy)
        path.MoveToPoint(p0.x, p0.y)
        # Next point is the left base of the arrow
        p1 = wx.Point(p0.x + H_ARROW * math.tan(math.radians(AA)),
                      p0.y - H_ARROW)
        path.AddLineToPoint(p1.x, p1.y)
        # Start of lower left rounded corner
        p2 = wx.Point(p1.x - ARROW_OFFSET + R, p1.y)
        path.AddLineToPoint(p2.x, p2.y)
        # The lower left rounded corner. p3 is the center of the arc
        p3 = wx.Point(p2.x, p2.y - R)
        path.AddArc(p3.x, p3.y, R, math.radians(90), math.radians(180), True)
        # The left side
        p4 = wx.Point(p3.x - R, p3.y - H + R)
        left_x = p4.x
        path.AddLineToPoint(p4.x, p4.y)
        # The upper left rounded corner. p5 is the center of the arc
        p5 = wx.Point(p4.x + R, p4.y)
        path.AddArc(p5.x, p5.y, R, math.radians(180), math.radians(-90), True)
        # The upper side
        p6 = wx.Point(p5.x + W - R, p5.y - R)
        top_y = p6.y
        path.AddLineToPoint(p6.x, p6.y)
        # The upper right rounded corner. p7 is the center of the arc
        p7 = wx.Point(p6.x, p6.y + R)
        path.AddArc(p7.x, p7.y, R, math.radians(-90), math.radians(0), True)
        # The right side
        p8 = wx.Point(p7.x + R, p7.y + H - R)
        path.AddLineToPoint(p8.x, p8.y)
        # The lower right rounded corner. p9 is the center of the arc
        p9 = wx.Point(p8.x - R, p8.y)
        path.AddArc(p9.x, p9.y, R, math.radians(0), math.radians(90), True)
        # The lower side
        p10 = wx.Point(p9.x - W + W_ARROW + ARROW_OFFSET, p9.y + R)
        path.AddLineToPoint(p10.x, p10.y)
        path.CloseSubpath()
        # Draw sharp lines on GTK which uses Cairo
        # See: http://www.cairographics.org/FAQ/#sharp_lines
        gc.Translate(0.5, 0.5)
        # Draw the ballon
        BORDER_COLOR = wx.Colour(127, 127, 127)
        BG_COLOR = wx.Colour(255, 255, 231)
        PEN = wx.Pen(BORDER_COLOR, 1, wx.PENSTYLE_SOLID)
        BRUSH = wx.Brush(BG_COLOR, wx.BRUSHSTYLE_SOLID)
        gc.SetPen(PEN)
        gc.SetBrush(BRUSH)
        gc.DrawPath(path)
        # Draw the pin
        if sticky:
            pin = wx.Bitmap(os.path.join(ICONS_DIR, "stickypin.png"))
        else:
            pin = wx.Bitmap(os.path.join(ICONS_DIR, "unstickypin.png"))
        self._dc.DrawBitmap(pin, p7.x - 5, p6.y + 5, True)

        # Return
        bx = left_x
        by = top_y
        bw = W + R + 1
        bh = H + R + H_ARROW + 1
        bounding_rect = wx.Rect(bx, by, bw, bh)
        return bounding_rect, left_x + BALLOON_RADIUS, top_y + BALLOON_RADIUS


def break_text(text, dc, max_width_in_px):
    """ Break the text into lines so that they fits within the given width."""
    sentences = text.split("\n")
    lines = []
    for sentence in sentences:
        w, _ = dc.GetTextExtent(sentence)
        if w <= max_width_in_px:
            lines.append(sentence)
        # The sentence is too long. Break it.
        else:
            break_sentence(dc, lines, sentence, max_width_in_px)
    return lines


def break_sentence(dc, lines, sentence, max_width_in_px):
    """Break a sentence into lines."""
    line = []
    max_word_len_in_ch = get_max_word_length(dc, max_width_in_px)
    words = break_line(dc, sentence, max_word_len_in_ch)
    for word in words:
        w, _ = dc.GetTextExtent("".join(line) + word + " ")
        # Max line length reached. Start a new line
        if w > max_width_in_px:
            lines.append("".join(line))
            line = []
        line.append(word + " ")
        # Word edning with '-' is a broken word. Start a new line
        if word.endswith('-'):
            lines.append("".join(line))
            line = []
    if len(line) > 0:
        lines.append("".join(line))


def break_line(dc, sentence, max_word_len_in_ch):
    """Break a sentence into words."""
    words = sentence.split(" ")
    new_words = []
    for word in words:
        broken_words = break_word(dc, word, max_word_len_in_ch)
        for broken_word in broken_words:
            new_words.append(broken_word)
    return new_words


def break_word(dc, word, max_word_len_in_ch):
    """
    Break words if they are too long.

    If a single word is too long to fit we have to break it.
    If not we just return the word given.
    """
    words = []
    while len(word) > max_word_len_in_ch:
        word1 = word[0:max_word_len_in_ch] + "-"
        word = word[max_word_len_in_ch:]
        words.append(word1)
    words.append(word)
    return words


def get_max_word_length(dc, max_width_in_px):
    TEMPLATE_CHAR = 'K'
    word = [TEMPLATE_CHAR]
    w, _ = dc.GetTextExtent("".join(word))
    while w < max_width_in_px:
        word.append(TEMPLATE_CHAR)
        w, _ = dc.GetTextExtent("".join(word))
    return len(word) - 1