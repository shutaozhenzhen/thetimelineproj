# Copyright (C) 2009, 2010, 2011  Rickard Lindberg, Roger Lindberg
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


from datetime import datetime
import re

from timelinelib.calendar.bosparanian import Bosparanian
from timelinelib.calendar.bosparanian import bosparanian_week
from timelinelib.calendar.bosparanian_monthnames import bosp_name_of_month
from timelinelib.calendar.bosparanian_monthnames import bosp_abbreviated_name_of_month
from timelinelib.calendar.bosparanian_weekdaynames import bosp_abbreviated_name_of_weekday
from timelinelib.data import TimeOutOfRangeLeftError
from timelinelib.data import TimeOutOfRangeRightError
from timelinelib.data import TimePeriod
from timelinelib.data import time_period_center
from timelinelib.drawing.interface import Strip
from timelinelib.time.timeline import delta_from_days
from timelinelib.time.typeinterface import TimeType
import timelinelib.calendar.bosparanian as bosparanian
import timelinelib.time.timeline as timeline
from timelinelib.calendar import get_date_formatter
from sys import stdout


class BosparanianTimeType(TimeType):

    def __init__(self):
        self.major_strip_is_decade = False

    def __eq__(self, other):
        return isinstance(other, BosparanianTimeType)

    def __ne__(self, other):
        return not (self == other)

    def time_string(self, time):
        return "%d-%02d-%02d %02d:%02d:%02d" % bosparanian.from_time(time).to_tuple()

    def parse_time(self, time_string):
        match = re.search(r"^(-?\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)$", time_string)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            hour = int(match.group(4))
            minute = int(match.group(5))
            second = int(match.group(6))
            try:
                return Bosparanian(year, month, day, hour, minute, second).to_time()
            except ValueError:
                raise ValueError("Invalid time, time string = '%s'" % time_string)
        else:
            raise ValueError("Time not on correct format = '%s'" % time_string)

    def get_navigation_functions(self):
        return [
            (_("Go to &1000 BF\tCtrl+T"), go_to_1000_fn),
            (_("Go to &Date...\tCtrl+G"), go_to_date_fn),
            ("SEP", None),
            (_("Backward\tPgUp"), backward_fn),
            (_("Forward\tPgDn"), forward_fn),
            (_("Forward One Wee&k\tCtrl+K"), forward_one_week_fn),
            (_("Back One &Week\tCtrl+W"), backward_one_week_fn),
            (_("Forward One Mont&h\tCtrl+h"), forward_one_month_fn),
            (_("Back One &Month\tCtrl+M"), backward_one_month_fn),
            (_("Forward One Yea&r\tCtrl+R"), forward_one_year_fn),
            (_("Back One &Year\tCtrl+Y"), backward_one_year_fn),
            ("SEP", None),
            (_("Fit Millennium"), fit_millennium_fn),
            (_("Fit Century"), fit_century_fn),
            (_("Fit Decade"), fit_decade_fn),
            (_("Fit Year"), fit_year_fn),
            (_("Fit Month"), fit_month_fn),
            (_("Fit Week"), fit_week_fn),
            (_("Fit Day"), fit_day_fn),
        ]

    def is_date_time_type(self):
        return True

    def format_period(self, time_period):
        """Returns a unicode string describing the time period."""
        def label_with_time(time):
            return u"%s %s" % (label_without_time(time), time_label(time))

        def label_without_time(time):
            bosparanian_datetime = bosparanian.from_time(time)
            return u"%s %s %s" % (bosparanian_datetime.day, bosp_abbreviated_name_of_month(bosparanian_datetime.month), bosparanian_datetime.year)

        def time_label(time):
            return "%02d:%02d" % time.get_time_of_day()[:-1]
        if time_period.is_period():
            if time_period.has_nonzero_time():
                label = u"%s to %s" % (label_with_time(time_period.start_time),
                                       label_with_time(time_period.end_time))
            else:
                label = u"%s to %s" % (label_without_time(time_period.start_time),
                                       label_without_time(time_period.end_time))
        else:
            if time_period.has_nonzero_time():
                label = u"%s" % label_with_time(time_period.start_time)
            else:
                label = u"%s" % label_without_time(time_period.start_time)
        return label

    def format_delta(self, delta):
        days = delta.get_days()
        hours = delta.get_hours()
        minutes = delta.get_minutes()
        collector = []
        if days == 1:
            collector.append(u"1 %s" % _("day"))
        elif days > 1:
            collector.append(u"%d %s" % (days, _("days")))
        if hours == 1:
            collector.append(u"1 %s" % _("hour"))
        elif hours > 1:
            collector.append(u"%d %s" % (hours, _("hours")))
        if minutes == 1:
            collector.append(u"1 %s" % _("minute"))
        elif minutes > 1:
            collector.append(u"%d %s" % (minutes, _("minutes")))
        delta_string = u" ".join(collector)
        if delta_string == "":
            delta_string = "0"
        return delta_string

    def get_min_time(self):
        return (timeline.get_min_time(), _("can't be before year 10"))

    def get_max_time(self):
        return (timeline.BosparanianTime(5369833, 0), _("can't be after year 9989"))

    def choose_strip(self, metrics, config):
        """
        Return a tuple (major_strip, minor_strip) for current time period and
        window size.
        """
        day_period = TimePeriod(self, timeline.BosparanianTime(0, 0), timeline.BosparanianTime(1, 0))
        one_day_width = metrics.calc_exact_width(day_period)
        self.major_strip_is_decade = False
        if one_day_width > 20000:
            return (StripHour(), StripMinute())
        elif one_day_width > 600:
            return (StripDay(), StripHour())
        elif one_day_width > 60:
            return (StripMonth(), StripWeekday())
        elif one_day_width > 25:
            return (StripMonth(), StripDay())
        elif one_day_width > 10:
            return (StripMonth(),StripWeek(config))
        elif one_day_width > 1.75:
            return (StripYear(), StripMonth())
        elif one_day_width > 0.5:
            return (StripYear(), StripQuarter())
        elif one_day_width > 0.12:
            self.major_strip_is_decade = True
            return (StripDecade(), StripYear())
        elif one_day_width > 0.012:
            return (StripCentury(), StripDecade())
        else:
            return (StripCentury(), StripCentury())

    def mult_timedelta(self, delta, num):
        return delta * num

    def get_default_time_period(self):
        return time_period_center(self, self.now(), delta_from_days(30))

    def now(self):
        return Bosparanian(1000, 1, 1, 12, 0, 0).to_time()

    def get_time_at_x(self, time_period, x_percent_of_width):
        """Return the time at pixel `x`."""
        return time_period.start_time + time_period.delta() * x_percent_of_width

    def div_timedeltas(self, delta1, delta2):
        return delta1 / delta2

    def get_max_zoom_delta(self):
        return (delta_from_days(1200 * 365), _("Can't zoom wider than 1200 years"))

    def get_min_zoom_delta(self):
        return (timeline.delta_from_seconds(60), _("Can't zoom deeper than 1 minute"))

    def get_zero_delta(self):
        return timeline.delta_from_seconds(0)

    def time_period_has_nonzero_time(self, time_period):
        nonzero_time = (time_period.start_time.seconds != 0 or
                        time_period.end_time.seconds != 0)
        return nonzero_time

    def get_name(self):
        return u"bosparaniantime"

    def get_duplicate_functions(self):
        return [
            (_("Day"), move_period_num_days),
            (_("Week"), move_period_num_weeks),
            (_("Month"), move_period_num_months),
            (_("Year"), move_period_num_years),
        ]

    def zoom_is_ok(self, delta):
        return (delta.seconds > 60) or (delta.get_days() > 0)

    def half_delta(self, delta):
        return delta / 2

    def margin_delta(self, delta):
        return delta / 24

    def event_date_string(self, time):
        bosparanian_time = bosparanian.from_time(time)
        return get_date_formatter().format(bosparanian_time.year, bosparanian_time.month, bosparanian_time.day)

    def event_time_string(self, time):
        bosparanian_time = bosparanian.from_time(time)
        return "%02d:%02d" % (bosparanian_time.hour, bosparanian_time.minute)

    def eventtimes_equals(self, time1, time2):
        s1 = "%s %s" % (self.event_date_string(time1),
                        self.event_date_string(time1))
        s2 = "%s %s" % (self.event_date_string(time2),
                        self.event_date_string(time2))
        return s1 == s2

    def adjust_for_bc_years(self, time):
        return time


def go_to_1000_fn(main_frame, current_period, navigation_fn):
    navigation_fn(lambda tp: tp.center(current_period.time_type.now()))


def go_to_date_fn(main_frame, current_period, navigation_fn):
    def navigate_to(time):
        navigation_fn(lambda tp: tp.center(time))
    main_frame.display_time_editor_dialog(
        BosparanianTimeType(), current_period.mean_time(), navigate_to, _("Go to Date"))


def backward_fn(main_frame, current_period, navigation_fn):
    _move_page_smart(current_period, navigation_fn, -1)


def forward_fn(main_frame, current_period, navigation_fn):
    _move_page_smart(current_period, navigation_fn, 1)


def _move_page_smart(current_period, navigation_fn, direction):
    if _whole_number_of_years(current_period):
        _move_page_years(current_period, navigation_fn, direction)
    elif _whole_number_of_months(current_period):
        _move_page_months(current_period, navigation_fn, direction)
    else:
        navigation_fn(lambda tp: tp.move_delta(direction * current_period.delta()))


def _whole_number_of_years(period):
    """
    >>> from timelinetest.utils import gregorian_period

    >>> _whole_number_of_years(gregorian_period("1 Jan 2013", "1 Jan 2014"))
    True

    >>> _whole_number_of_years(gregorian_period("1 Jan 2013", "1 Jan 2015"))
    True

    >>> _whole_number_of_years(gregorian_period("1 Feb 2013", "1 Feb 2014"))
    False

    >>> _whole_number_of_years(gregorian_period("1 Jan 2013", "1 Feb 2014"))
    False
    """
    return (bosparanian.from_time(period.start_time).is_praios_first() and
            bosparanian.from_time(period.end_time).is_praios_first() and
            _calculate_year_diff(period) > 0)


def _move_page_years(curret_period, navigation_fn, direction):
    def navigate(tp):
        year_delta = direction * _calculate_year_diff(curret_period)
        bosparanian_start = bosparanian.from_time(curret_period.start_time)
        bosparanian_end = bosparanian.from_time(curret_period.end_time)
        new_start_year = bosparanian_start.year + year_delta
        new_end_year = bosparanian_end.year + year_delta
        try:
            new_start = bosparanian_start.replace(year=new_start_year).to_time()
            new_end = bosparanian_end.replace(year=new_end_year).to_time()
            if new_end > curret_period.time_type.get_max_time()[0]:
                raise ValueError()
            if new_start < curret_period.time_type.get_min_time()[0]:
                raise ValueError()
        except ValueError:
            if direction < 0:
                raise TimeOutOfRangeLeftError()
            else:
                raise TimeOutOfRangeRightError()
        return tp.update(new_start, new_end)
    navigation_fn(navigate)


def _calculate_year_diff(period):
    return (bosparanian.from_time(period.end_time).year -
            bosparanian.from_time(period.start_time).year)


def _whole_number_of_months(period):
    """
    >>> from timelinetest.utils import gregorian_period

    >>> _whole_number_of_months(gregorian_period("1 Jan 2013", "1 Jan 2014"))
    True

    >>> _whole_number_of_months(gregorian_period("1 Jan 2013", "1 Mar 2014"))
    True

    >>> _whole_number_of_months(gregorian_period("2 Jan 2013", "2 Mar 2014"))
    False

    >>> _whole_number_of_months(gregorian_period("1 Jan 2013 12:00", "1 Mar 2014"))
    False
    """
    start, end = bosparanian.from_time(period.start_time), bosparanian.from_time(period.end_time)
    start_months = start.year * 13 + start.month
    end_months = end.year * 13 + end.month
    month_diff = end_months - start_months
    return (start.is_first_of_month() and
            end.is_first_of_month() and
            month_diff > 0)


def _move_page_months(curret_period, navigation_fn, direction):
    def navigate(tp):
        start = bosparanian.from_time(curret_period.start_time)
        end = bosparanian.from_time(curret_period.end_time)
        start_months = start.year * 13 + start.month
        end_months = end.year * 13 + end.month
        month_diff = end_months - start_months
        month_delta = month_diff * direction
        new_start_year, new_start_month = _months_to_year_and_month(start_months + month_delta)
        new_end_year, new_end_month = _months_to_year_and_month(end_months + month_delta)
        try:
            new_start = start.replace(year=new_start_year, month=new_start_month)
            new_end = end.replace(year=new_end_year, month=new_end_month)
            start = new_start.to_time()
            end = new_end.to_time()
            if end > curret_period.time_type.get_max_time()[0]:
                raise ValueError()
            if start < curret_period.time_type.get_min_time()[0]:
                raise ValueError()
        except ValueError:
            if direction < 0:
                raise TimeOutOfRangeLeftError()
            else:
                raise TimeOutOfRangeRightError()
        return tp.update(start, end)
    navigation_fn(navigate)


def _months_to_year_and_month(months):
    years = int(months / 13)
    month = months - years * 13
    if month == 0:
        month = 13
        years -= 1
    return years, month


def forward_one_week_fn(main_frame, current_period, navigation_fn):
    wk = delta_from_days(7)
    navigation_fn(lambda tp: tp.move_delta(wk))


def backward_one_week_fn(main_frame, current_period, navigation_fn):
    wk = delta_from_days(7)
    navigation_fn(lambda tp: tp.move_delta(-1 * wk))


def navigate_month_step(current_period, navigation_fn, direction):
    """
    Currently does notice leap years.
    """
    # TODO: NEW-TIME: (year, month, day, hour, minute, second) -> int (days in # month)
    tm = current_period.mean_time()
    gt = bosparanian.from_time(tm)
    mv=delta_from_days(gt.days_in_month())
    navigation_fn(lambda tp: tp.move_delta(direction * mv))


def forward_one_month_fn(main_frame, current_period, navigation_fn):
    navigate_month_step(current_period, navigation_fn, 1)


def backward_one_month_fn(main_frame, current_period, navigation_fn):
    navigate_month_step(current_period, navigation_fn, -1)


def forward_one_year_fn(main_frame, current_period, navigation_fn):
    yr = delta_from_days(365)
    navigation_fn(lambda tp: tp.move_delta(yr))


def backward_one_year_fn(main_frame, current_period, navigation_fn):
    yr = delta_from_days(365)
    navigation_fn(lambda tp: tp.move_delta(-1 * yr))


def fit_millennium_fn(main_frame, current_period, navigation_fn):
    mean = bosparanian.from_time(current_period.mean_time())
    if mean.year > get_millenium_max_year():
        year = get_millenium_max_year()
    else:
        year = max(get_min_year_containing_jan_1(), int(mean.year / 1000) * 1000)
    start = bosparanian.from_date(year, 1, 1).to_time()
    end = bosparanian.from_date(year + 1000, 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def get_min_year_containing_praios_1():
    return bosparanian.from_time(BosparanianTimeType().get_min_time()[0]).year + 1


def get_millenium_max_year():
    return bosparanian.from_time(BosparanianTimeType().get_max_time()[0]).year - 1000


def get_century_max_year():
    return bosparanian.from_time(BosparanianTimeType().get_max_time()[0]).year - 100


def fit_century_fn(main_frame, current_period, navigation_fn):
    mean = bosparanian.from_time(current_period.mean_time())
    if mean.year > get_century_max_year():
        year = get_century_max_year()
    else:
        year = max(get_min_year_containing_praios_1(), int(mean.year / 100) * 100)
    start = bosparanian.from_date(year, 1, 1).to_time()
    end = bosparanian.from_date(year + 100, 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def fit_decade_fn(main_frame, current_period, navigation_fn):
    mean = bosparanian.from_time(current_period.mean_time())
    start = bosparanian.from_date(int(mean.year / 10) * 10, 1, 1).to_time()
    end = bosparanian.from_date(int(mean.year / 10) * 10 + 10, 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def fit_year_fn(main_frame, current_period, navigation_fn):
    mean = bosparanian.from_time(current_period.mean_time())
    start = bosparanian.from_date(mean.year, 1, 1).to_time()
    end = bosparanian.from_date(mean.year + 1, 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def fit_month_fn(main_frame, current_period, navigation_fn):
    mean = bosparanian.from_time(current_period.mean_time())
    start = bosparanian.from_date(mean.year, mean.month, 1).to_time()
    if mean.month == 13:
        end = bosparanian.from_date(mean.year + 1, 1, 1).to_time()
    else:
        end = bosparanian.from_date(mean.year, mean.month + 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def fit_day_fn(main_frame, current_period, navigation_fn):
    mean = bosparanian.from_time(current_period.mean_time())
    start = bosparanian.from_date(mean.year, mean.month, mean.day).to_time()
    end = start + delta_from_days(1)
    navigation_fn(lambda tp: tp.update(start, end))


def fit_week_fn(main_frame, current_period, navigation_fn):
    mean = bosparanian.from_time(current_period.mean_time())
    start = bosparanian.from_date(mean.year, mean.month, mean.day).to_time()
    weekday = start.get_day_of_week()
    start = start - delta_from_days(weekday)
    if not main_frame.week_starts_on_monday():
        start = start - delta_from_days(1)
    end = start + delta_from_days(7)
    navigation_fn(lambda tp: tp.update(start, end))


class StripCentury(Strip):

    def label(self, time, major=False):
        if major:
            # TODO: This only works for English. Possible to localize?
            time = bosparanian.from_time(time)
            start_year = self._century_start_year(time.year)
            century = (start_year + 100) / 100
            if century <= 0:
                century -= 1
            return str(century) + " century BF"
        return ""

    def start(self, time):
        time = bosparanian.from_time(time)
        return bosparanian.from_date(self._century_start_year(time.year), 1, 1).to_time()

    def increment(self, time):
        gregorian_time = bosparanian.from_time(time)
        return gregorian_time.replace(year=gregorian_time.year + 100).to_time()

    def _century_start_year(self, year):
        year = (int(year) / 100) * 100
        return year


class StripDecade(Strip):

    def label(self, time, major=False):
        time = bosparanian.from_time(time)
        return format_decade(self._decade_start_year(time.year))

    def start(self, time):
        bosparanian_time = bosparanian.from_time(time)
        new_bosparanian = bosparanian.from_date(self._decade_start_year(bosparanian_time.year), 1, 1)
        return new_bosparanian.to_time()

    def increment(self, time):
        bosparanian_time = bosparanian.from_time(time)
        return bosparanian_time.replace(year=bosparanian_time.year + 10).to_time()

    def _decade_start_year(self, year):
        # The first start year must be to the left of the first visible
        # year on the timeline in order to draw the first vertical decade
        # line correctly. Therefore -10 in the calculation below
        return (int(year) / 10) * 10 - 10


class StripYear(Strip):

    def label(self, time, major=False):
        return format_year(bosparanian.from_time(time).year)

    def start(self, time):
        bosparanian_time = bosparanian.from_time(time)
        new_bosparanian = bosparanian.from_date(bosparanian_time.year, 1, 1)
        return new_bosparanian.to_time()

    def increment(self, time):
        bosparanian_time = bosparanian.from_time(time)
        return bosparanian_time.replace(year=bosparanian_time.year + 1).to_time()


class StripMonth(Strip):

    def label(self, time, major=False):
        time = bosparanian.from_time(time)
        if major:
            return "%s %s" % (bosp_name_of_month(time.month),
                              format_year(time.year))
        if time.month == 13:
            return bosp_abbreviated_name_of_month(time.month)
        return bosp_name_of_month(time.month)

    def start(self, time):
        bosparanian_time = bosparanian.from_time(time)
        new_bosparanian = bosparanian.from_date(bosparanian_time.year, bosparanian_time.month, 1)
        return new_bosparanian.to_time()

    def increment(self, time):
        days_in_month = bosparanian.from_time(time).days_in_month()
        return time + delta_from_days(days_in_month)

#    def get_font(self, time_period):
#        if (bosparanian.from_time(time_period.start_time).month == 1):
#            return get_default_font(8, True)
#        else:
#            return get_default_font(8)

class StripQuarter(Strip):
    
    def get_quarter(self,time):
        m = bosparanian.from_time(time).month;
        if m == 13:
            return 0
        return (m - 1) // 3 + 1

    def label(self, time, major=False):
        q = self.get_quarter(time)
        if q == 0:
            return "NLD"
        return "Q%d"%q

    def start(self, time):
        q = self.get_quarter(time)
        if q == 0:
            m = 13
        else:
            m = (q - 1) * 3 + 1
        return bosparanian.from_date(bosparanian.from_time(time).year, m, 1).to_time()

    def increment(self, time):
        q = self.get_quarter(time)
        if q == 0:
            days_in_quarter = 5
        else:
            days_in_quarter = 30 * 3
        return time + delta_from_days(days_in_quarter)


class StripDay(Strip):

    def label(self, time, major=False):
        time = bosparanian.from_time(time)
        if major:
            return "%s %s %s" % (time.day,
                                 bosp_abbreviated_name_of_month(time.month),
                                 format_year(time.year))
        return str(time.day)

    def start(self, time):
        bosparanian_time = bosparanian.from_time(time)
        new_bosparanian = bosparanian.from_date(bosparanian_time.year, bosparanian_time.month, bosparanian_time.day)
        return new_bosparanian.to_time()

    def increment(self, time):
        return time + delta_from_days(1)

#    def get_font(self, time_period):
#        if (time_period.start_time.get_day_of_week() == 0): # Windsday in italics (start of week)
#            return get_default_font(8,True,False)
#        elif (time_period.start_time.get_day_of_week() == 3): # Praiosday in bold
#            return get_default_font(8, True, True)
#        else:
#            return get_default_font(8)


class StripWeek(Strip):

    def __init__(self, config):
        Strip.__init__(self)
        self.config = config

    def label(self, time, major=False):
        if major:
            first_weekday = self.start(time)
            next_first_weekday = self.increment(first_weekday)
            last_weekday = next_first_weekday - delta_from_days(1)
            range_string = self._time_range_string(first_weekday, last_weekday)
            return (_("Week") + " %s (%s)") % (bosparanian_week(time), range_string)
        return _("Week") + " %s" % bosparanian_week(time)

    def _time_range_string(self, start, end):
        start = bosparanian.from_time(start)
        end = bosparanian.from_time(end)
        if start.year == end.year:
            if start.month == end.month:
                return "%s-%s %s %s" % (start.day, end.day,
                                        bosp_abbreviated_name_of_month(start.month),
                                        format_year(start.year))
            return "%s %s-%s %s %s" % (start.day,
                                       bosp_abbreviated_name_of_month(start.month),
                                       end.day,
                                       bosp_abbreviated_name_of_month(end.month),
                                       format_year(start.year))
        return "%s %s %s-%s %s %s" % (start.day,
                                      bosp_abbreviated_name_of_month(start.month),
                                      format_year(start.year),
                                      end.day,
                                      bosp_abbreviated_name_of_month(end.month),
                                      format_year(end.year))

    def start(self, time):
        days_to_subtract = time.get_day_of_week()
        return timeline.BosparanianTime(time.julian_day - days_to_subtract, 0)

    def increment(self, time):
        return time + delta_from_days(7)


class StripWeekday(Strip):

    def label(self, time, major=False):
        if major:
            day_of_week = time.get_day_of_week()
            time = bosparanian.from_time(time)
            return "%s %s %s %s" % (bosp_abbreviated_name_of_weekday(day_of_week),
                                    time.day,
                                    bosp_abbreviated_name_of_month(time.month),
                                    format_year(time.year))
        return (bosp_abbreviated_name_of_weekday(time.get_day_of_week()) +
                " %s" % bosparanian.from_time(time).day)

    def start(self, time):
        bosparanian_time = bosparanian.from_time(time)
        new_bosparanian = bosparanian.from_date(bosparanian_time.year, bosparanian_time.month, bosparanian_time.day)
        return new_bosparanian.to_time()

    def increment(self, time):
        return time + delta_from_days(1)

#    def get_font(self, time_period):
#        if (time_period.start_time.get_day_of_week() == 0): # Windsday in italics (start of week)
#            return get_default_font(8,True,False)
#        elif (time_period.start_time.get_day_of_week() == 3): # Praiosday in bold
#            return get_default_font(8, True, True)
#        else:
#            return get_default_font(8)


class StripHour(Strip):

    def label(self, time, major=False):
        time = bosparanian.from_time(time)
        if major:
            return "%s %s %s: %sh" % (time.day, bosp_abbreviated_name_of_month(time.month),
                                      format_year(time.year), time.hour)
        return str(time.hour)

    def start(self, time):
        (hours, _, _) = time.get_time_of_day()
        return timeline.BosparanianTime(time.julian_day, hours * 60 * 60)

    def increment(self, time):
        return time + timeline.delta_from_seconds(60 * 60)


class StripMinute(Strip):

    def label(self, time, major=False):
        time = bosparanian.from_time(time)
        if major:
            return "%s %s %s: %s:%s" % (time.day, bosp_abbreviated_name_of_month(time.month),
                                        format_year(time.year), time.hour, time.minute)
        return str(time.minute)

    def start(self, time):
        (hours, minutes, _) = time.get_time_of_day()
        return timeline.BosparanianTime(time.julian_day, minutes * 60 + hours * 60 * 60)

    def increment(self, time):
        return time + timeline.delta_from_seconds(60)


def format_year(year):
    return "%dBF" % year


def format_decade(start_year):
    return str(start_year + 10) + "s"


def move_period_num_days(period, num):
    delta = delta_from_days(1) * num
    start_time = period.start_time + delta
    end_time = period.end_time + delta
    return TimePeriod(period.time_type, start_time, end_time)


def move_period_num_weeks(period, num):
    delta = delta_from_days(7) * num
    start_time = period.start_time + delta
    end_time = period.end_time + delta
    return TimePeriod(period.time_type, start_time, end_time)


def move_period_num_months(period, num):
    try:
        delta = num
        years = abs(delta) / 13
        bosparanian_start = bosparanian.from_time(period.start_time)
        bosparanian_end = bosparanian.from_time(period.end_time)
        if num < 0:
            years = -years
        delta = delta - 13 * years
        if delta < 0:
            start_month = bosparanian_start.month + 13 + delta
            end_month = bosparanian_end.month + 13 + delta
            if start_month > 13:
                start_month -= 13
                end_month -= 13
            if start_month > bosparanian_start.month:
                years -= 1
        else:
            start_month = bosparanian_start.month + delta
            end_month = bosparanian_start.month + delta
            if start_month > 13:
                start_month -= 13
                end_month -= 13
                years += 1
        start_year = bosparanian_start.year + years
        end_year = bosparanian_start.year + years
        start_time = bosparanian_start.replace(year=start_year, month=start_month)
        end_time = bosparanian_end.replace(year=end_year, month=end_month)
        return TimePeriod(period.time_type, start_time.to_time(), end_time.to_time())
    except ValueError:
        return None


def move_period_num_years(period, num):
    try:
        delta = num
        start_year = bosparanian.from_time(period.start_time).year
        end_year = bosparanian.from_time(period.end_time).year
        start_time = bosparanian.from_time(period.start_time).replace(year=start_year + delta)
        end_time = bosparanian.from_time(period.end_time).replace(year=end_year + delta)
        return TimePeriod(period.time_type, start_time.to_time(), end_time.to_time())
    except ValueError:
        return None
