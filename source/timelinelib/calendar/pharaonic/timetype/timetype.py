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


from datetime import datetime
import re

from timelinelib.calendar.gregorian.timetype import GregorianTimeType
from timelinelib.calendar.pharaonic.pharaonic import PharaonicDateTime
from timelinelib.calendar.pharaonic.monthnames import abbreviated_name_of_month
from timelinelib.calendar.pharaonic.time import PharaonicDelta
from timelinelib.calendar.pharaonic.time import PharaonicTime
from timelinelib.calendar.pharaonic.time import SECONDS_IN_DAY
from timelinelib.canvas.data import TimeOutOfRangeLeftError
from timelinelib.canvas.data import TimeOutOfRangeRightError
from timelinelib.canvas.data import TimePeriod
from timelinelib.canvas.data import time_period_center
from timelinelib.calendar.gregorian.gregorian import gregorian_ymd_to_julian_day
from timelinelib.calendar.pharaonic.pharaonic import julian_day_to_pharaonic_ymd
from timelinelib.calendar.gregorian.timetype.durationformatter import DurationFormatter
from timelinelib.calendar.gregorian.timetype.durationtype import YEARS, DAYS, HOURS, MINUTES, SECONDS
from timelinelib.calendar.pharaonic.timetype.strips.stripcentury import StripCentury
from timelinelib.calendar.pharaonic.timetype.strips.stripweek import StripWeek
from timelinelib.calendar.pharaonic.timetype.strips.stripweekday import StripWeekday
from timelinelib.calendar.pharaonic.timetype.strips.stripminute import StripMinute
from timelinelib.calendar.pharaonic.timetype.strips.stripday import StripDay
from timelinelib.calendar.pharaonic.timetype.strips.stripdecade import StripDecade
from timelinelib.calendar.pharaonic.timetype.strips.striphour import StripHour
from timelinelib.calendar.pharaonic.timetype.strips.stripmonth import StripMonth
from timelinelib.calendar.pharaonic.timetype.strips.stripyear import StripYear
from timelinelib.calendar.pharaonic.timetype.formatters import format_year, get_day_of_week


class PharaonicTimeType(GregorianTimeType):

    def __eq__(self, other):
        return isinstance(other, PharaonicTimeType)

    def time_string(self, time):
        return "%d-%02d-%02d %02d:%02d:%02d" % PharaonicDateTime.from_time(time).to_tuple()

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
                return PharaonicDateTime(year, month, day, hour, minute, second).to_time()
            except ValueError:
                raise ValueError("Invalid time, time string = '%s'" % time_string)
        else:
            raise ValueError("Time not on correct format = '%s'" % time_string)

    def get_navigation_functions(self):
        return [
            (_("Go to &Today") + "\tCtrl+T", go_to_today_fn),
            (_("Go to &Date...") + "\tCtrl+G", go_to_date_fn),
            ("SEP", None),
            (_("Backward") + "\tPgUp", backward_fn),
            (_("Forward") + "\tPgDn", forward_fn),
            (_("Forward One Wee&k") + "\tCtrl+K", forward_one_week_fn),
            (_("Back One &Week") + "\tCtrl+W", backward_one_week_fn),
            (_("Forward One Mont&h") + "\tCtrl+H", forward_one_month_fn),
            (_("Back One &Month") + "\tCtrl+M", backward_one_month_fn),
            (_("Forward One Yea&r") + "\tCtrl+R", forward_one_year_fn),
            (_("Back One &Year") + "\tCtrl+Y", backward_one_year_fn),
            ("SEP", None),
            (_("Fit Millennium"), fit_millennium_fn),
            (_("Fit Century"), create_strip_fitter(StripCentury)),
            (_("Fit Decade"), create_strip_fitter(StripDecade)),
            (_("Fit Year"), create_strip_fitter(StripYear)),
            (_("Fit Month"), create_strip_fitter(StripMonth)),
            (_("Fit Week"), fit_week_fn),
            (_("Fit Day"), create_strip_fitter(StripDay)),
        ]

    def format_period(self, time_period):
        """Returns a unicode string describing the time period."""
        def label_with_time(time):
            return "%s %s" % (label_without_time(time), time_label(time))

        def label_without_time(time):
            pharaonic_datetime = PharaonicDateTime.from_time(time)
            return "%s %s %s" % (
                pharaonic_datetime.day,
                abbreviated_name_of_month(pharaonic_datetime.month),
                format_year(pharaonic_datetime.year)
            )

        def time_label(time):
            return "%02d:%02d" % time.get_time_of_day()[:-1]
        if time_period.is_period():
            if has_nonzero_time(time_period):
                label = "%s to %s" % (label_with_time(time_period.start_time),
                                      label_with_time(time_period.end_time))
            else:
                label = "%s to %s" % (label_without_time(time_period.start_time),
                                      label_without_time(time_period.end_time))
        else:
            if has_nonzero_time(time_period):
                label = "%s" % label_with_time(time_period.start_time)
            else:
                label = "%s" % label_without_time(time_period.start_time)
        return label

    def format_delta(self, delta):
        days = abs(delta.get_days())
        seconds = abs(delta.seconds) - days * SECONDS_IN_DAY
        delta_format = (YEARS, DAYS, HOURS, MINUTES, SECONDS)
        return DurationFormatter([days, seconds]).format(delta_format)

    def get_min_time(self):
        return PharaonicTime.min()

    def get_max_time(self):
        return PharaonicTime(5369833, 0)

    def choose_strip(self, metrics, appearance):
        """
        Return a tuple (major_strip, minor_strip) for current time period and
        window size.
        """
        day_period = TimePeriod(PharaonicTime(0, 0),PharaonicTime(1, 0))
        one_day_width = metrics.calc_exact_width(day_period)
        if one_day_width > 20000:
            return StripHour(), StripMinute()
        elif one_day_width > 600:
            return StripDay(), StripHour()
        elif one_day_width > 45:
            return StripWeek(appearance), StripWeekday()
        elif one_day_width > 25:
            return StripMonth(), StripDay()
        elif one_day_width > 1.5:
            return StripYear(), StripMonth()
        elif one_day_width > 0.12:
            return StripDecade(), StripYear()
        elif one_day_width > 0.012:
            return StripCentury(), StripDecade()
        else:
            return StripCentury(), StripCentury()

    def get_default_time_period(self):
        return time_period_center(self.now(), PharaonicDelta.from_days(30))

    def supports_saved_now(self):
        return False

    def set_saved_now(self, time):
        ()

    def now(self):
        py = datetime.now()
        julian_day = gregorian_ymd_to_julian_day(py.year, py.month, py.day)
        year, month, day = julian_day_to_pharaonic_ymd(julian_day)
        pharaonic = PharaonicDateTime(
            year,
            month,
            day,
            py.hour,
            py.minute,
            py.second
        )
        return pharaonic.to_time()

    def get_min_zoom_delta(self):
        return PharaonicDelta.from_seconds(60), _("Can't zoom deeper than 1 minute")

    def get_name(self):
        return "pharaonic"

    def get_duplicate_functions(self):
        return [
            (_("Day"), move_period_num_days),
            (_("Week"), move_period_num_weeks),
            (_("Month"), move_period_num_months),
            (_("Year"), move_period_num_years),
        ]

    def is_special_day(self, time):
        return False

    """TO DO: the last day of the month, not week, are considered weekends in the pharaonic calendar. Currently the last two days of the week are considered weekends.
    """
    def is_weekend_day(self, time):
        pharaonic_time = PharaonicDateTime.from_time(time)
        return pharaonic_time.day in (9, 10, 19, 20, 29, 30)

    def create_time_picker(self, parent, *args, **kwargs):
        from timelinelib.calendar.pharaonic.timepicker.datetimepicker import PharaonicDateTimePicker
        return PharaonicDateTimePicker(parent, *args, **kwargs)

    def create_period_picker(self, parent, *args, **kwargs):
        from timelinelib.calendar.pharaonic.timepicker.periodpicker import PharaonicPeriodPicker
        return PharaonicPeriodPicker(parent, *args, **kwargs)


def go_to_today_fn(main_frame, current_period, navigation_fn):
    navigation_fn(lambda tp: tp.center(PharaonicTimeType().now()))


def go_to_date_fn(main_frame, current_period, navigation_fn):
    def navigate_to(time):
        navigation_fn(lambda tp: tp.center(time))
    main_frame.display_time_editor_dialog(
        PharaonicTimeType(), current_period.mean_time(), navigate_to, _("Go to Date"))


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
    >>> from timelinelib.test.utils import gregorian_period

    >>> _whole_number_of_years(gregorian_period("13 Jun 287", "12 Jun 288"))
    True

    >>> _whole_number_of_years(gregorian_period("24 Apr 490", "24 Apr 491"))
    True

    >>> _whole_number_of_years(gregorian_period("8 Dec 1776", "8 Dec 1777"))
    False

    >>> _whole_number_of_years(gregorian_period("6 Sep 2013", "11 Sep 2014"))
    False
    """
    return (PharaonicDateTime.from_time(period.start_time).is_first_day_in_year() and
            PharaonicDateTime.from_time(period.end_time).is_first_day_in_year() and
            _calculate_year_diff(period) > 0)


def _move_page_years(curret_period, navigation_fn, direction):
    def navigate(tp):
        year_delta = direction * _calculate_year_diff(curret_period)
        pharaonic_start = PharaonicDateTime.from_time(curret_period.start_time)
        pharaonic_end = PharaonicDateTime.from_time(curret_period.end_time)
        new_start_year = pharaonic_start.year + year_delta
        new_end_year = pharaonic_end.year + year_delta
        try:
            new_start = pharaonic_start.replace(year=new_start_year).to_time()
            new_end = pharaonic_end.replace(year=new_end_year).to_time()
            if new_end > PharaonicTimeType().get_max_time():
                raise ValueError()
            if new_start < PharaonicTimeType().get_min_time():
                raise ValueError()
        except ValueError:
            if direction < 0:
                raise TimeOutOfRangeLeftError()
            else:
                raise TimeOutOfRangeRightError()
        return tp.update(new_start, new_end)
    navigation_fn(navigate)


def _calculate_year_diff(period):
    return (PharaonicDateTime.from_time(period.end_time).year -
            PharaonicDateTime.from_time(period.start_time).year)


def _whole_number_of_months(period):

    """
>>> from timelinelib.test.utils import gregorian_period

    >>> _whole_number_of_months(gregorian_period("24 May 490", "23 Jun 490"))
    True

    >>> _whole_number_of_months(gregorian_period("16 Aug 1", "21 Aug 1	"))
    True

    >>> _whole_number_of_months(gregorian_period("2 Jan 2013", "2 Mar 2014"))
    False

    >>> _whole_number_of_months(gregorian_period("1 Jan 2013 12:00", "1 Mar 2014"))
    False
    """
    start, end = PharaonicDateTime.from_time(period.start_time), PharaonicDateTime.from_time(period.end_time)
    start_months = start.year * 13 + start.month
    end_months = end.year * 13 + end.month
    month_diff = end_months - start_months

    return (start.is_first_of_month() and
            end.is_first_of_month() and
            month_diff > 0)


def _move_page_months(curret_period, navigation_fn, direction):
    def navigate(tp):
        start = PharaonicDateTime.from_time(curret_period.start_time)
        end = PharaonicDateTime.from_time(curret_period.end_time)
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
            if end > PharaonicTimeType().get_max_time():
                raise ValueError()
            if start < PharaonicTimeType().get_min_time():
                raise ValueError()
        except ValueError:
            if direction < 0:
                raise TimeOutOfRangeLeftError()
            else:
                raise TimeOutOfRangeRightError()
        return tp.update(start, end)
    navigation_fn(navigate)


def _months_to_year_and_month(months):
    years = int(months // 13)
    month = months - years * 13
    if month == 0:
        month = 13
        years -= 1
    return years, month


def forward_one_week_fn(main_frame, current_period, navigation_fn):
    wk = PharaonicDelta.from_days(10)
    navigation_fn(lambda tp: tp.move_delta(wk))


def backward_one_week_fn(main_frame, current_period, navigation_fn):
    wk = PharaonicDelta.from_days(7)
    navigation_fn(lambda tp: tp.move_delta(-1 * wk))


def navigate_month_step(current_period, navigation_fn, direction):
    
    # TODO: NEW-TIME: (year, month, day, hour, minute, second) -> int (days in # month)
    tm = current_period.mean_time()
    pt = PharaonicDateTime.from_time(tm)
    if pt.month == 13:
        d = 5
    d = 30
    
    mv = PharaonicDelta.from_days(d)
    navigation_fn(lambda tp: tp.move_delta(direction * mv))


def forward_one_month_fn(main_frame, current_period, navigation_fn):
    navigate_month_step(current_period, navigation_fn, 1)


def backward_one_month_fn(main_frame, current_period, navigation_fn):
    navigate_month_step(current_period, navigation_fn, -1)


def forward_one_year_fn(main_frame, current_period, navigation_fn):
    yr = PharaonicDelta.from_days(365)
    navigation_fn(lambda tp: tp.move_delta(yr))


def backward_one_year_fn(main_frame, current_period, navigation_fn):
    yr = PharaonicDelta.from_days(365)
    navigation_fn(lambda tp: tp.move_delta(-1 * yr))


def fit_millennium_fn(main_frame, current_period, navigation_fn):
    mean = PharaonicDateTime.from_time(current_period.mean_time())
    if mean.year > get_millenium_max_year():
        year = get_millenium_max_year()
    else:
        year = max(get_min_year_containing_jan_1(), int(mean.year // 1000) * 1000)
    start = PharaonicDateTime.from_ymd(year, 1, 1).to_time()
    end = PharaonicDateTime.from_ymd(year + 1000, 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def get_min_year_containing_jan_1():
    return PharaonicDateTime.from_time(PharaonicTimeType().get_min_time()).year + 1


def get_millenium_max_year():
    return PharaonicDateTime.from_time(PharaonicTimeType().get_max_time()).year - 1000


def fit_week_fn(main_frame, current_period, navigation_fn):
    mean = PharaonicDateTime.from_time(current_period.mean_time())
    start = PharaonicDateTime.from_ymd(mean.year, mean.month, mean.day).to_time()
    weekday = get_day_of_week(start)
    start = start - PharaonicDelta.from_days(weekday)
    if not main_frame.week_starts_on_monday():
        start = start - PharaonicDelta.from_days(1)
    end = start + PharaonicDelta.from_days(10)
    navigation_fn(lambda tp: tp.update(start, end))


def create_strip_fitter(strip_cls):
    def fit(main_frame, current_period, navigation_fn):
        def navigate(time_period):
            strip = strip_cls()
            start = strip.start(current_period.mean_time())
            end = strip.increment(start)
            return time_period.update(start, end)
        navigation_fn(navigate)
    return fit


def move_period_num_days(period, num):
    delta = PharaonicDelta.from_days(1) * num
    start_time = period.start_time + delta
    end_time = period.end_time + delta
    return TimePeriod(start_time, end_time)


def move_period_num_weeks(period, num):
    delta = PharaonicDelta.from_days(7) * num
    start_time = period.start_time + delta
    end_time = period.end_time + delta
    return TimePeriod(start_time, end_time)


def move_period_num_months(period, num):
    def move_time(time):
        pharaonic_time = PharaonicDateTime.from_time(time)
        new_month = pharaonic_time.month + num
        new_year = pharaonic_time.year
        while new_month < 1:
            new_month += 13
            new_year -= 1
        while new_month > 13:
            new_month -= 13
            new_year += 1
        return pharaonic_time.replace(year=new_year, month=new_month).to_time()
    try:
        return TimePeriod(
            move_time(period.start_time),
            move_time(period.end_time)
        )
    except ValueError:
        return None


def move_period_num_years(period, num):
    try:
        delta = num
        start_year = PharaonicDateTime.from_time(period.start_time).year
        end_year = PharaonicDateTime.from_time(period.end_time).year
        start_time = PharaonicDateTime.from_time(period.start_time).replace(year=start_year + delta)
        end_time = PharaonicDateTime.from_time(period.end_time).replace(year=end_year + delta)
        return TimePeriod(start_time.to_time(), end_time.to_time())
    except ValueError:
        return None


def has_nonzero_time(time_period):
    return (time_period.start_time.seconds != 0 or
            time_period.end_time.seconds != 0)
