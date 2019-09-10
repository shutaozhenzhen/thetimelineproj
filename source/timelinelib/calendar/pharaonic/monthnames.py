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


ENGLISH_MONTH_NAMES = [
    "Thoth",
    "Paopi",
    "Hathor",
    "Koiak",
    "Tobi",
    "Meshir",
    "Paremhat",
    "Parmouti",
    "Pashons",
    "Paoni",
    "Epip",
    "Mesori",
    "Pi Kogi",
]


def _(message):
    return message  # deferred translation


ABBREVIATED_ENGLISH_MONTH_NAMES = [
    "I Akhet",
    "II Akhet",
    "III Akhet",
    "IV Akhet",
    "I Peret",
    "II Peret",
    "III Peret",
    "IV Peret",
    "I Shemu",
    "II Shemu",
    "III Shemu",
    "IV Shemu",
    "- -",
]
del _


def month_from_english_name(month_name):
    return ENGLISH_MONTH_NAMES.index(month_name) + 1


def english_name_of_month(month):
    return ENGLISH_MONTH_NAMES[month - 1]


def abbreviated_name_of_month(month):
    return _(ABBREVIATED_ENGLISH_MONTH_NAMES[month - 1])


def month_of_abbreviated_name(name):
    for month in range(1, 13):
        if abbreviated_name_of_month(month) == name:
            return month
    raise ValueError("Could not find month name %s." % name)
