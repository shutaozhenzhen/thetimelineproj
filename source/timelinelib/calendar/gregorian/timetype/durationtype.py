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


class DurationType:

    def __init__(self, name, single_name, value_fn, remainder_fn):
        self._name = name
        self._single_name = single_name
        self._value_fn = value_fn
        self._remainder_fn = remainder_fn

    @property
    def name(self):
        return self._name

    @property
    def single_name(self):
        return self._single_name

    @property
    def value_fn(self):
        return self._value_fn

    @property
    def remainder_fn(self):
        return self._remainder_fn


YEARS = DurationType(_('years'), _('year'),
                     lambda ds: ds[0] // 365,
                     lambda ds: (ds[0] % 365, ds[1]))
MONTHS = DurationType(_('months'), _('month'),
                      lambda ds: ds[0] // 30,
                      lambda ds: (ds[0] % 30, ds[1]))
WEEKS = DurationType(_('weeks'), _('week'),
                     lambda ds: ds[0] // 7,
                     lambda ds: (ds[0] % 7, ds[1]))
DAYS = DurationType(_('days'), _('day'),
                    lambda ds: ds[0],
                    lambda ds: (0, ds[1]))
HOURS = DurationType(_('hours'), _('hour'),
                     lambda ds: ds[0] * 24 + ds[1] // 3600,
                     lambda ds: (0, ds[1] % 3600))
MINUTES = DurationType(_('minutes'), _('minute'),
                       lambda ds: ds[0] * 1440 + ds[1] // 60,
                       lambda ds: (0, ds[1] % 60))
SECONDS = DurationType(_('seconds'), _('second'),
                       lambda ds: ds[0] * 86400 + ds[1],
                       lambda ds: (0, 0))
