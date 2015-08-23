import sys
import os.path
from timelinelib.calendar.gregorian import GregorianUtils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

if __name__ == "__main__":
    for julian_day in range(10000000):
        (year, month, day) = GregorianUtils.from_absolute_day(julian_day)
        roundtrip_julian_day = GregorianUtils.to_julian_day(year, month, day)
        print("%d - %d-%d-%d - %d" % (julian_day, year, month, day, roundtrip_julian_day))
