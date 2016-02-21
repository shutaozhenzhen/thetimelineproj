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


class DateFormatParser(object):

    def parse(self, date_format):
        if self.is_valid(date_format):
            return (self.separator1, self.separator2)
        else:
            return None

    def get_error_text(self):
        return _("""\
Invalid Date Format:

The format should contain
    one year placeholder  = yyyy
    one month placeholder = mmm or mm
    one day placeholder   = dd
    two placeholders for separators between year, mont and day

Separators can't contain the lsetters y, m or d

Example of valid formats:
    yyyy-mm-dd
    dd/mm/yyyy
    mmm/dd-yyyy
        """)

    def is_valid(self, date_format):
        monthname = False
        fmt = date_format.lower()
        if "yyyy" in fmt:
            fmt = fmt.replace("yyyy", "", 1)
        else:
            return False
        if "mmm" in fmt:
            fmt = fmt.replace("mmm", "", 1)
            monthname = True
        elif "mm" in fmt:
            fmt = fmt.replace("mm", "", 1)
        else:
            return False
        if "dd" in fmt:
            fmt = fmt.replace("dd", "", 1)
        else:
            return False
        if "y" in fmt or "m" in fmt or "d" in fmt:
            return False
        year_index = date_format.lower().index("yyyy")
        year_lenght = 4
        if monthname:
            month_index = date_format.lower().index("mmm")
            month_length = 3
        else:
            month_index = date_format.lower().index("mm")
            month_length = 2
        day_index = date_format.lower().index("dd")
        day_length = 2
        self.separator1 = ""
        self.separator2 = ""
        if year_index == 0:
            if month_index < day_index:
                self.separator1 = date_format[year_lenght:month_index]
                self.separator2 = date_format[month_index + month_length:day_index]
            else:
                self.separator1 = date_format[year_lenght:day_index]
                self.separator2 = date_format[day_index + day_length:month_index]
        elif month_index == 0:
            if year_index < day_index:
                self.separator1 = date_format[month_length:year_index]
                self.separator2 = date_format[year_index + year_lenght:day_index]
            else:
                self.separator1 = date_format[month_length:day_index]
                self.separator2 = date_format[day_index + day_length:year_index]
        elif day_index == 0:
            if month_index < year_index:
                self.separator1 = date_format[day_length:month_index]
                self.separator2 = date_format[month_index + month_length:year_index]
            else:
                self.separator1 = date_format[day_length:year_index]
                self.separator2 = date_format[year_index + year_lenght:month_index]
        else:
            return False
        fmt = fmt.replace(self.separator1, "", 1)
        fmt = fmt.replace(self.separator2, "", 1)
        if len(fmt) > 0:
            return False
        return True
