
class CalendarBase(object):
    
    def replace(self, year=None, month=None):
        raise NotImplementedError("replace not implemented.")

    def days_in_month(self):
        raise NotImplementedError("days_in_month not implemented.")
    
    def to_tuple(self):
        raise NotImplementedError("to_tuple not implemented.")

    def to_date_tuple(self):
        raise NotImplementedError("to_date_tuple not implemented.")

    def to_time_tuple(self):
        raise NotImplementedError("to_time_tuple not implemented.")

    def to_time(self):
        raise NotImplementedError("to_time not implemented.")

    def is_first_of_month(self):
        raise NotImplementedError("is_first_of_month not implemented.")

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.to_tuple() == other.to_tuple())

    def __repr__(self):
        raise NotImplementedError("__repr__ not implemented.")


class CalendarUtilsBase(object):
    @classmethod
    def is_valid(self, year, month, day):
        raise NotImplementedError("is_valid not implemented.")
    
    @classmethod    
    def is_valid_time(self, hour, minute, second):
        raise NotImplementedError("is_valid_time not implemented.")
    
    @classmethod
    def days_in_month(self, year, month):
        raise NotImplementedError("days_in_month not implemented.")
    
    @classmethod
    def is_leap_year(year):
        raise NotImplementedError("is_leap_year not implemented.")
    
    @classmethod
    def from_absolute_day(self, absolute_day):
        raise NotImplementedError("from_absolute_day not implemented.")
    
    @classmethod
    def to_absolute_day(self, year, month, day):
        raise NotImplementedError("to_absolute_day not implemented.")
    
    @classmethod
    def calendar_week(self, time):
        raise NotImplementedError("calendar_week not implemented.")
    
    @classmethod
    def from_time(self, time):
        raise NotImplementedError("from_time not implemented.")
    
    @classmethod
    def from_date(self, year, month, day):
        raise NotImplementedError("from_date not implemented")
    