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

from timelinelib.calendar.gregorian.gregorian import GregorianDateTime
from timelinelib.calendar.gregorian.monthnames import abbreviated_name_of_month
from timelinelib.calendar.gregorian.time import GregorianDelta
from timelinelib.calendar.gregorian.time import GregorianTime
from timelinelib.calendar.gregorian.time import SECONDS_IN_DAY
from timelinelib.calendar.timetype import TimeType
from timelinelib.canvas.data import TimeOutOfRangeLeftError
from timelinelib.canvas.data import TimeOutOfRangeRightError
from timelinelib.canvas.data import TimePeriod
from timelinelib.canvas.data import time_period_center
from timelinelib.calendar.gregorian.timetype import DurationFormatter
from timelinelib.calendar.gregorian.timetype.durationtype import YEARS, DAYS, HOURS, MINUTES, SECONDS
from timelinelib.calendar.gregorian.timetype.strips import StripMinute
from timelinelib.calendar.gregorian.timetype.strips import StripHour
from timelinelib.calendar.gregorian.timetype.strips import StripWeekday
from timelinelib.calendar.gregorian.timetype.strips import StripWeek
from timelinelib.calendar.gregorian.timetype.strips import StripDay
from timelinelib.calendar.gregorian.timetype.strips import StripMonth
from timelinelib.calendar.gregorian.timetype.strips import StripYear
from timelinelib.calendar.gregorian.timetype.strips import StripDecade
from timelinelib.calendar.gregorian.timetype.strips import StripCentury
from timelinelib.calendar.gregorian.timetype.yearformatter import format_year, BC


class GregorianTimeType(TimeType):

    DURATION_TYPE_HOURS = _('Hours')
    DURATION_TYPE_WORKDAYS = _('Workdays')
    DURATION_TYPE_DAYS = _('Days')
    DURATION_TYPE_MINUTES = _('Minutes')
    DURATION_TYPE_SECONDS = _('Seconds')

    def __eq__(self, other):
        return isinstance(other, GregorianTimeType)

    def __ne__(self, other):
        return not (self == other)

    def time_string(self, time):
        return "%d-%02d-%02d %02d:%02d:%02d" % GregorianDateTime.from_time(time).to_tuple()

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
                return GregorianDateTime(year, month, day, hour, minute, second).to_time()
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
            gregorian_datetime = GregorianDateTime.from_time(time)
            return "%s %s %s" % (
                gregorian_datetime.day,
                abbreviated_name_of_month(gregorian_datetime.month),
                format_year(gregorian_datetime.year)
            )

        def time_label(time):
            return "%02d:%02d" % time.get_time_of_day()[:-1]

        if time_period.is_period():
            if time_period.has_nonzero_time():
                label = "%s to %s" % (label_with_time(time_period.start_time),
                                      label_with_time(time_period.end_time))
            else:
                label = "%s to %s" % (label_without_time(time_period.start_time),
                                      label_without_time(time_period.end_time))
        else:
            if time_period.has_nonzero_time():
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
        return GregorianTime.min()

    def get_max_time(self):
        return GregorianTime(5369833, 0)

    def choose_strip(self, metrics, appearance):
        """
        Return a tuple (major_strip, minor_strip) for current time period and
        window size.
        """
        day_period = TimePeriod(GregorianTime(0, 0), GregorianTime(1, 0))
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
        return time_period_center(self.now(), GregorianDelta.from_days(30))

    def supports_saved_now(self):
        return False

    def set_saved_now(self, time):
        ()

    def now(self):
        py = datetime.now()
        gregorian = GregorianDateTime(
            py.year,
            py.month,
            py.day,
            py.hour,
            py.minute,
            py.second
        )
        return gregorian.to_time()

    def get_min_zoom_delta(self):
        return GregorianDelta.from_seconds(60), _("Can't zoom deeper than 1 minute")

    def get_name(self):
        return "gregoriantime"

    def get_duplicate_functions(self):
        return [
            (_("Day"), move_period_num_days),
            (_("Week"), move_period_num_weeks),
            (_("Month"), move_period_num_months),
            (_("Year"), move_period_num_years),
        ]

    def is_special_day(self, time):
        return False

    def is_weekend_day(self, time):
        return time.is_weekend_day

    def create_time_picker(self, parent, *args, **kwargs):
        from timelinelib.calendar.gregorian.timepicker.datetimepicker import GregorianDateTimePicker
        return GregorianDateTimePicker(parent, *args, **kwargs)

    def create_period_picker(self, parent, *args, **kwargs):
        from timelinelib.calendar.gregorian.timepicker.periodpicker import GregorianPeriodPicker
        return GregorianPeriodPicker(parent, *args, **kwargs)

    def get_duration_types(self):
        return [
            self.DURATION_TYPE_HOURS,
            self.DURATION_TYPE_WORKDAYS,
            self.DURATION_TYPE_DAYS,
            self.DURATION_TYPE_MINUTES,
            self.DURATION_TYPE_SECONDS]

    def get_duration_divisor(self, duration_type):
        return {
            self.DURATION_TYPE_SECONDS: 1,
            self.DURATION_TYPE_MINUTES: 60,
            self.DURATION_TYPE_HOURS: 3600,
            self.DURATION_TYPE_DAYS: 86400,
            self.DURATION_TYPE_WORKDAYS: 28800,
        }[duration_type]


def go_to_today_fn(main_frame, current_period, navigation_fn):
    navigation_fn(lambda tp: tp.center(GregorianTimeType().now()))


def go_to_date_fn(main_frame, current_period, navigation_fn):
    def navigate_to(time):
        navigation_fn(lambda tp: tp.center(time))
    main_frame.display_time_editor_dialog(
        GregorianTimeType(), current_period.mean_time(), navigate_to, _("Go to Date"))


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

    >>> _whole_number_of_years(gregorian_period("1 Jan 2013", "1 Jan 2014"))
    True

    >>> _whole_number_of_years(gregorian_period("1 Jan 2013", "1 Jan 2015"))
    True

    >>> _whole_number_of_years(gregorian_period("1 Feb 2013", "1 Feb 2014"))
    False

    >>> _whole_number_of_years(gregorian_period("1 Jan 2013", "1 Feb 2014"))
    False
    """
    return (GregorianDateTime.from_time(period.start_time).is_first_day_in_year() and
            GregorianDateTime.from_time(period.end_time).is_first_day_in_year() and
            _calculate_year_diff(period) > 0)


def _move_page_years(curret_period, navigation_fn, direction):
    def navigate(tp):
        year_delta = direction * _calculate_year_diff(curret_period)
        gregorian_start = GregorianDateTime.from_time(curret_period.start_time)
        gregorian_end = GregorianDateTime.from_time(curret_period.end_time)
        new_start_year = gregorian_start.year + year_delta
        new_end_year = gregorian_end.year + year_delta
        try:
            new_start = gregorian_start.replace(year=new_start_year).to_time()
            new_end = gregorian_end.replace(year=new_end_year).to_time()
            if new_end > GregorianTimeType().get_max_time():
                raise ValueError()
            if new_start < GregorianTimeType().get_min_time():
                raise ValueError()
        except ValueError:
            if direction < 0:
                raise TimeOutOfRangeLeftError()
            else:
                raise TimeOutOfRangeRightError()
        return tp.update(new_start, new_end)
    navigation_fn(navigate)


def _calculate_year_diff(period):
    return (GregorianDateTime.from_time(period.end_time).year -
            GregorianDateTime.from_time(period.start_time).year)


def _whole_number_of_months(period):
    """
    >>> from timelinelib.test.utils import gregorian_period

    >>> _whole_number_of_months(gregorian_period("1 Jan 2013", "1 Jan 2014"))
    True

    >>> _whole_number_of_months(gregorian_period("1 Jan 2013", "1 Mar 2014"))
    True

    >>> _whole_number_of_months(gregorian_period("2 Jan 2013", "2 Mar 2014"))
    False

    >>> _whole_number_of_months(gregorian_period("1 Jan 2013 12:00", "1 Mar 2014"))
    False
    """
    start, end = GregorianDateTime.from_time(period.start_time), GregorianDateTime.from_time(period.end_time)
    start_months = start.year * 12 + start.month
    end_months = end.year * 12 + end.month
    month_diff = end_months - start_months
    return (start.is_first_of_month() and
            end.is_first_of_month() and
            month_diff > 0)


def _move_page_months(curret_period, navigation_fn, direction):
    def navigate(tp):
        start = GregorianDateTime.from_time(curret_period.start_time)
        end = GregorianDateTime.from_time(curret_period.end_time)
        start_months = start.year * 12 + start.month
        end_months = end.year * 12 + end.month
        month_diff = end_months - start_months
        month_delta = month_diff * direction
        new_start_year, new_start_month = _months_to_year_and_month(start_months + month_delta)
        new_end_year, new_end_month = _months_to_year_and_month(end_months + month_delta)
        try:
            new_start = start.replace(year=new_start_year, month=new_start_month)
            new_end = end.replace(year=new_end_year, month=new_end_month)
            start = new_start.to_time()
            end = new_end.to_time()
            if end > GregorianTimeType().get_max_time():
                raise ValueError()
            if start < GregorianTimeType().get_min_time():
                raise ValueError()
        except ValueError:
            if direction < 0:
                raise TimeOutOfRangeLeftError()
            else:
                raise TimeOutOfRangeRightError()
        return tp.update(start, end)
    navigation_fn(navigate)


def _months_to_year_and_month(months):
    years = int(months // 12)
    month = months - years * 12
    if month == 0:
        month = 12
        years -= 1
    return years, month


def forward_one_week_fn(main_frame, current_period, navigation_fn):
    wk = GregorianDelta.from_days(7)
    navigation_fn(lambda tp: tp.move_delta(wk))


def backward_one_week_fn(main_frame, current_period, navigation_fn):
    wk = GregorianDelta.from_days(7)
    navigation_fn(lambda tp: tp.move_delta(-1 * wk))


def navigate_month_step(current_period, navigation_fn, direction):
    """
    Currently does notice leap years.
    """
    # TODO: NEW-TIME: (year, month, day, hour, minute, second) -> int (days in # month)
    tm = current_period.mean_time()
    gt = GregorianDateTime.from_time(tm)
    if direction > 0:
        if gt.month == 2:
            d = 28
        elif gt.month in (4, 6, 9, 11):
            d = 30
        else:
            d = 31
    else:
        if gt.month == 3:
            d = 28
        elif gt.month in (5, 7, 10, 12):
            d = 30
        else:
            d = 31
    mv = GregorianDelta.from_days(d)
    navigation_fn(lambda tp: tp.move_delta(direction * mv))


def forward_one_month_fn(main_frame, current_period, navigation_fn):
    navigate_month_step(current_period, navigation_fn, 1)


def backward_one_month_fn(main_frame, current_period, navigation_fn):
    navigate_month_step(current_period, navigation_fn, -1)


def forward_one_year_fn(main_frame, current_period, navigation_fn):
    yr = GregorianDelta.from_days(365)
    navigation_fn(lambda tp: tp.move_delta(yr))


def backward_one_year_fn(main_frame, current_period, navigation_fn):
    yr = GregorianDelta.from_days(365)
    navigation_fn(lambda tp: tp.move_delta(-1 * yr))


def fit_millennium_fn(main_frame, current_period, navigation_fn):
    mean = GregorianDateTime.from_time(current_period.mean_time())
    if mean.year > get_millenium_max_year():
        year = get_millenium_max_year()
    else:
        year = max(get_min_year_containing_jan_1(), int(mean.year // 1000) * 1000)
    start = GregorianDateTime.from_ymd(year, 1, 1).to_time()
    end = GregorianDateTime.from_ymd(year + 1000, 1, 1).to_time()
    navigation_fn(lambda tp: tp.update(start, end))


def get_min_year_containing_jan_1():
    return GregorianDateTime.from_time(GregorianTimeType().get_min_time()).year + 1


def get_millenium_max_year():
    return GregorianDateTime.from_time(GregorianTimeType().get_max_time()).year - 1000


def fit_week_fn(main_frame, current_period, navigation_fn):
    mean = GregorianDateTime.from_time(current_period.mean_time())
    start = GregorianDateTime.from_ymd(mean.year, mean.month, mean.day).to_time()
    weekday = start.day_of_week
    start = start - GregorianDelta.from_days(weekday)
    if not main_frame.week_starts_on_monday():
        start = start - GregorianDelta.from_days(1)
    end = start + GregorianDelta.from_days(7)
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
    delta = GregorianDelta.from_days(1) * num
    start_time = period.start_time + delta
    end_time = period.end_time + delta
    return TimePeriod(start_time, end_time)


def move_period_num_weeks(period, num):
    delta = GregorianDelta.from_days(7) * num
    start_time = period.start_time + delta
    end_time = period.end_time + delta
    return TimePeriod(start_time, end_time)


def move_period_num_months(period, num):
    def move_time(time):
        gregorian_time = GregorianDateTime.from_time(time)
        new_month = gregorian_time.month + num
        new_year = gregorian_time.year
        while new_month < 1:
            new_month += 12
            new_year -= 1
        while new_month > 12:
            new_month -= 12
            new_year += 1
        return gregorian_time.replace(year=new_year, month=new_month).to_time()
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
        start_year = GregorianDateTime.from_time(period.start_time).year
        end_year = GregorianDateTime.from_time(period.end_time).year
        start_time = GregorianDateTime.from_time(period.start_time).replace(year=start_year + delta)
        end_time = GregorianDateTime.from_time(period.end_time).replace(year=end_year + delta)
        return TimePeriod(start_time.to_time(), end_time.to_time())
    except ValueError:
        return None
