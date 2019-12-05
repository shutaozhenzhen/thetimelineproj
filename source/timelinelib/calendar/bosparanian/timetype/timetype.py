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


import re

from timelinelib.calendar.bosparanian.bosparanian import BosparanianDateTime
from timelinelib.calendar.bosparanian.monthnames import bosp_abbreviated_name_of_month
from timelinelib.calendar.bosparanian.time import BosparanianDelta
from timelinelib.calendar.bosparanian.time import BosparanianTime
from timelinelib.calendar.gregorian.timetype.durationtype import DAYS
from timelinelib.calendar.gregorian.timetype import DurationFormatter
from timelinelib.calendar.gregorian.timetype.durationtype import HOURS
from timelinelib.calendar.gregorian.timetype.durationtype import MINUTES
from timelinelib.calendar.gregorian.timetype.durationtype import SECONDS
from timelinelib.calendar.gregorian.timetype import SECONDS_IN_DAY
from timelinelib.calendar.gregorian.timetype.durationtype import YEARS
from timelinelib.calendar.timetype import TimeType
from timelinelib.canvas.data import TimeOutOfRangeLeftError
from timelinelib.canvas.data import TimeOutOfRangeRightError
from timelinelib.canvas.data import TimePeriod
from timelinelib.canvas.data import time_period_center
from timelinelib.calendar.bosparanian.timetype.strips.stripcentury import StripCentury
from timelinelib.calendar.bosparanian.timetype.strips.stripdecade import StripDecade
from timelinelib.calendar.bosparanian.timetype.strips.stripquarter import StripQuarter
from timelinelib.calendar.bosparanian.timetype.strips.stripyear import StripYear
from timelinelib.calendar.bosparanian.timetype.strips.stripmonth import StripMonth
from timelinelib.calendar.bosparanian.timetype.strips.stripweek import StripWeek
from timelinelib.calendar.bosparanian.timetype.strips.stripweekday import StripWeekday
from timelinelib.calendar.bosparanian.timetype.strips.stripday import StripDay
from timelinelib.calendar.bosparanian.timetype.strips.striphour import StripHour
from timelinelib.calendar.bosparanian.timetype.strips.stripminute import StripMinute


class BosparanianTimeType(TimeType):

    def __init__(self):
        self.major_strip_is_decade = False
        self.saved_now = None

    def __eq__(self, other):
        return isinstance(other, BosparanianTimeType)

    def __ne__(self, other):
        return not (self == other)

    def time_string(self, time):
        return "%d-%02d-%02d %02d:%02d:%02d" % BosparanianDateTime.from_time(time).to_tuple()

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
                return BosparanianDateTime(year, month, day, hour, minute, second).to_time()
            except ValueError:
                raise ValueError("Invalid time, time string = '%s'" % time_string)
        else:
            raise ValueError("Time not on correct format = '%s'" % time_string)

    def get_navigation_functions(self):
        return [
            (_("Open &Now Date Editor") + "\tCtrl+T", open_now_date_editor),
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
            (_("Fit Century"), fit_century_fn),
            (_("Fit Decade"), fit_decade_fn),
            (_("Fit Year"), fit_year_fn),
            (_("Fit Month"), fit_month_fn),
            (_("Fit Week"), fit_week_fn),
            (_("Fit Day"), fit_day_fn),
            ("SEP", None),
        ]

    def format_period(self, time_period):
        """Returns a unicode string describing the time period."""
        def label_with_time(time):
            return "%s %s" % (label_without_time(time), time_label(time))

        def label_without_time(time):
            bosparanian_datetime = BosparanianDateTime.from_time(time)
            return "%s %s %s" % (bosparanian_datetime.day, bosp_abbreviated_name_of_month(bosparanian_datetime.month), bosparanian_datetime.year)

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
        return BosparanianTime.min()

    def get_max_time(self):
        return BosparanianTime(5369833, 0)

    def choose_strip(self, metrics, appearance):
        """
        Return a tuple (major_strip, minor_strip) for current time period and
        window size.
        """
        day_period = TimePeriod(BosparanianTime(0, 0), BosparanianTime(1, 0))
        one_day_width = metrics.calc_exact_width(day_period)
        self.major_strip_is_decade = False
        if one_day_width > 20000:
            return StripHour(), StripMinute()
        elif one_day_width > 600:
            return StripDay(), StripHour()
        elif one_day_width > 60:
            return StripMonth(), StripWeekday()
        elif one_day_width > 25:
            return StripMonth(), StripDay()
        elif one_day_width > 10:
            return StripMonth(), StripWeek()
        elif one_day_width > 1.75:
            return StripYear(), StripMonth()
        elif one_day_width > 0.5:
            return StripYear(), StripQuarter()
        elif one_day_width > 0.12:
            self.major_strip_is_decade = True
            return StripDecade(), StripYear()
        elif one_day_width > 0.012:
            return StripCentury(), StripDecade()
        else:
            return StripCentury(), StripCentury()

    def get_default_time_period(self):
        return time_period_center(self.now(), BosparanianDelta.from_days(30))

    def supports_saved_now(self):
        return True

    def set_saved_now(self, time):
        self.saved_now = time

    def now(self):
        if self.saved_now is None:
            return BosparanianDateTime(1000, 1, 1, 12, 0, 0).to_time()
        return self.saved_now

    def get_min_zoom_delta(self):
        return BosparanianDelta.from_seconds(60), _("Can't zoom deeper than 1 minute")

    def get_name(self):
        return "bosparaniantime"

    def get_duplicate_functions(self):
        return [
            (_("Day"), move_period_num_days),
            (_("Week"), move_period_num_weeks),
            (_("Month"), move_period_num_months),
            (_("Year"), move_period_num_years),
        ]

    def is_special_day(self, time):
        return self.get_day_of_week(time) == 3

    def is_weekend_day(self, time):
        return self.get_day_of_week(time) in (0, 3)

    def get_day_of_week(self, time):
        return time.julian_day % 7

    def create_time_picker(self, parent, *args, **kwargs):
        from timelinelib.calendar.bosparanian.timepicker import BosparanianDateTimePicker
        return BosparanianDateTimePicker(parent, *args, **kwargs)

    def create_period_picker(self, parent, *args, **kwargs):
        from timelinelib.calendar.bosparanian.periodpicker import BosparanianPeriodPicker
        return BosparanianPeriodPicker(parent, *args, **kwargs)


def open_now_date_editor(main_frame, current_period, navigation_fn):
    def navigate_to(time):
        navigation_fn(lambda tp: tp.center(time))
    main_frame.display_now_date_editor_dialog(navigate_to, _("Change Now Date"))


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
    return (BosparanianDateTime.from_time(period.start_time).is_first_day_in_year() and
            BosparanianDateTime.from_time(period.end_time).is_first_day_in_year() and
            _calculate_year_diff(period) > 0)


def _move_page_years(curret_period, navigation_fn, direction):
    def navigate(tp):
        year_delta = direction * _calculate_year_diff(curret_period)
        bosparanian_start = BosparanianDateTime.from_time(curret_period.start_time)
        bosparanian_end = BosparanianDateTime.from_time(curret_period.end_time)
        new_start_year = bosparanian_start.year + year_delta
        new_end_year = bosparanian_end.year + year_delta
        try:
            new_start = bosparanian_start.replace(year=new_start_year).to_time()
            new_end = bosparanian_end.replace(year=new_end_year).to_time()
            if new_end > BosparanianTimeType().get_max_time():
                raise ValueError()
            if new_start < BosparanianTimeType().get_min_time():
                raise ValueError()
        except ValueError:
            if direction < 0:
                raise TimeOutOfRangeLeftError()
            else:
                raise TimeOutOfRangeRightError()
        return tp.update(new_start, new_end)
    navigation_fn(navigate)


def _calculate_year_diff(period):
    return (BosparanianDateTime.from_time(period.end_time).year -
            BosparanianDateTime.from_time(period.start_time).year)


def _whole_number_of_months(period):
    start, end = BosparanianDateTime.from_time(period.start_time), BosparanianDateTime.from_time(period.end_time)
    start_months = start.year * 13 + start.month
    end_months = end.year * 13 + end.month
    month_diff = end_months - start_months
    return (start.is_first_of_month() and
            end.is_first_of_month() and
            month_diff > 0)


def _move_page_months(curret_period, navigation_fn, direction):
    def navigate(tp):
        start = BosparanianDateTime.from_time(curret_period.start_time)
        end = BosparanianDateTime.from_time(curret_period.end_time)
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
            if end > BosparanianTimeType().get_max_time():
                raise ValueError()
            if start < BosparanianTimeType().get_min_time():
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
    wk = BosparanianDelta.from_days(7)
    navigation_fn(lambda tp: tp.move_delta(wk))


def backward_one_week_fn(main_frame, current_period, navigation_fn):
    wk = BosparanianDelta.from_days(7)
    navigation_fn(lambda tp: tp.move_delta(-1 * wk))


def navigate_month_step(current_period, navigation_fn, direction):
    tm = current_period.mean_time()
    gt = BosparanianDateTime.from_time(tm)
    mv = BosparanianDelta.from_days(gt.days_in_month())
    navigation_fn(lambda tp: tp.move_delta(direction * mv))


def forward_one_month_fn(main_frame, current_period, navigation_fn):
    navigate_month_step(current_period, navigation_fn, 1)


def backward_one_month_fn(main_frame, current_period, navigation_fn):
    navigate_month_step(current_period, navigation_fn, -1)


def forward_one_year_fn(main_frame, current_period, navigation_fn):
    yr = BosparanianDelta.from_days(365)
    navigation_fn(lambda tp: tp.move_delta(yr))


def backward_one_year_fn(main_frame, current_period, navigation_fn):
    yr = BosparanianDelta.from_days(365)
    navigation_fn(lambda tp: tp.move_delta(-1 * yr))


def fit_millennium_fn(main_frame, current_period, navigation_fn):
    mean = BosparanianDateTime.from_time(current_period.mean_time())
    if mean.year > get_millenium_max_year():
        year = get_millenium_max_year()
    else:
        year = max(get_min_year_containing_praios_1(), int(mean.year // 1000) * 1000)
    start = BosparanianDateTime.from_ymd(year, 1, 1).to_time()
    end = BosparanianDateTime.from_ymd(year + 1000, 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def get_min_year_containing_praios_1():
    return BosparanianDateTime.from_time(BosparanianTimeType().get_min_time()).year + 1


def get_millenium_max_year():
    return BosparanianDateTime.from_time(BosparanianTimeType().get_max_time()).year - 1000


def get_century_max_year():
    return BosparanianDateTime.from_time(BosparanianTimeType().get_max_time()).year - 100


def fit_century_fn(main_frame, current_period, navigation_fn):
    mean = BosparanianDateTime.from_time(current_period.mean_time())
    if mean.year > get_century_max_year():
        year = get_century_max_year()
    else:
        year = max(get_min_year_containing_praios_1(), int(mean.year // 100) * 100)
    start = BosparanianDateTime.from_ymd(year, 1, 1).to_time()
    end = BosparanianDateTime.from_ymd(year + 100, 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def fit_decade_fn(main_frame, current_period, navigation_fn):
    mean = BosparanianDateTime.from_time(current_period.mean_time())
    start = BosparanianDateTime.from_ymd(int(mean.year // 10) * 10, 1, 1).to_time()
    end = BosparanianDateTime.from_ymd(int(mean.year // 10) * 10 + 10, 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def fit_year_fn(main_frame, current_period, navigation_fn):
    mean = BosparanianDateTime.from_time(current_period.mean_time())
    start = BosparanianDateTime.from_ymd(mean.year, 1, 1).to_time()
    end = BosparanianDateTime.from_ymd(mean.year + 1, 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def fit_month_fn(main_frame, current_period, navigation_fn):
    mean = BosparanianDateTime.from_time(current_period.mean_time())
    start = BosparanianDateTime.from_ymd(mean.year, mean.month, 1).to_time()
    if mean.month == 13:
        end = BosparanianDateTime.from_ymd(mean.year + 1, 1, 1).to_time()
    else:
        end = BosparanianDateTime.from_ymd(mean.year, mean.month + 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def fit_day_fn(main_frame, current_period, navigation_fn):
    mean = BosparanianDateTime.from_time(current_period.mean_time())
    start = BosparanianDateTime.from_ymd(mean.year, mean.month, mean.day).to_time()
    end = start + BosparanianDelta.from_days(1)
    navigation_fn(lambda tp: tp.update(start, end))


def fit_week_fn(main_frame, current_period, navigation_fn):
    mean = BosparanianDateTime.from_time(current_period.mean_time())
    start = BosparanianDateTime.from_ymd(mean.year, mean.month, mean.day).to_time()
    weekday = BosparanianTimeType().get_day_of_week(start)
    start = start - BosparanianDelta.from_days(weekday)
    if not main_frame.week_starts_on_monday():
        start = start - BosparanianDelta.from_days(1)
    end = start + BosparanianDelta.from_days(7)
    navigation_fn(lambda tp: tp.update(start, end))


def move_period_num_days(period, num):
    delta = BosparanianDelta.from_days(1) * num
    start_time = period.start_time + delta
    end_time = period.end_time + delta
    return TimePeriod(start_time, end_time)


def move_period_num_weeks(period, num):
    delta = BosparanianDelta.from_days(7) * num
    start_time = period.start_time + delta
    end_time = period.end_time + delta
    return TimePeriod(start_time, end_time)


def move_period_num_months(period, num):
    try:
        delta = num
        years = int(abs(delta)) // 13
        bosparanian_start = BosparanianDateTime.from_time(period.start_time)
        bosparanian_end = BosparanianDateTime.from_time(period.end_time)
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
        return TimePeriod(start_time.to_time(), end_time.to_time())
    except ValueError:
        return None


def move_period_num_years(period, num):
    try:
        delta = num
        start_year = BosparanianDateTime.from_time(period.start_time).year
        end_year = BosparanianDateTime.from_time(period.end_time).year
        start_time = BosparanianDateTime.from_time(period.start_time).replace(year=start_year + delta)
        end_time = BosparanianDateTime.from_time(period.end_time).replace(year=end_year + delta)
        return TimePeriod(start_time.to_time(), end_time.to_time())
    except ValueError:
        return None


def has_nonzero_time(time_period):
    return (time_period.start_time.seconds != 0 or
            time_period.end_time.seconds != 0)
