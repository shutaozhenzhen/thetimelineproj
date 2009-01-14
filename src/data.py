"""
Custom data types.
"""


from datetime import timedelta


# To save computation power (used by `delta_to_microseconds`)
US_PER_SEC = 1000000
US_PER_DAY = 24 * 60 * 60 * US_PER_SEC


class Timeline(object):
    """
    Base class that represents the interface for a timeline.

    A possible implementation could be for a timeline stored in a flat file or
    in a SQL database.

    In order to get an implementation, the `get_timeline` factory method should
    be used.

    All methods that modify the timeline should automatically save it.
    """

    def get_events(self, time_period):
        """Return all events visible within the time period."""
        pass

    def add_event(self, event):
        """Add `event` to the timeline."""
        pass

    def event_edited(self, event):
        """Notify that `event` has been modified so that it can be saved."""
        pass

    def delete_selected_events(self):
        """Delete all events that are selected."""
        pass

    def get_categories(self):
        """Return all available categories."""
        pass

    def add_category(self, category):
        """Add `category` to the timeline."""
        pass

    def category_edited(self, category):
        """Notify that `category` has been modified so that it can be saved."""
        pass

    def delete_category(self, category):
        """Delete `category` and remove it from all events."""
        pass

    def get_preferred_period(self):
        """Return the preferred period to display of this timeline."""
        pass

    def set_preferred_period(self, period):
        """Set the preferred period to display of this timeline."""
        pass

    def reset_selection(self):
        """Reset any selection on the timeline."""
        pass


class Event(object):
    """Represents an event on a timeline."""

    def __init__(self, start_time, end_time, text, category=None):
        """
        Create an event.
        
        `start_time` and `end_time` should be of the type datetime.
        """
        self.selected = False
        self.update(start_time, end_time, text, category)

    def update(self, start_time, end_time, text, category=None):
        self.time_period = TimePeriod(start_time, end_time)
        self.text = text
        self.category = category

    def inside_period(self, time_period):
        return self.time_period.overlap(time_period)

    def is_period(self):
        return self.time_period.is_period()

    def mean_time(self):
        return self.time_period.mean_time()


class Category(object):
    """Represent a category that an event belongs to."""

    def __init__(self, name, color):
        """
        Create a category with the given name and color.

        name = string
        color = (r, g, b)
        """
        self.name = name
        self.color = color


class TimePeriod(object):
    """
    """

    MAX_DIFF = timedelta(120 * 365) # 120 years
    MIN_DIFF = timedelta(hours=1) # 1 hour

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        if start_time > end_time:
            raise Exception("Invalid time period")

    def inside(self, time):
        return time >= self.start_time and time <= self.end_time

    def overlap(self, time_period):
        return not (time_period.end_time < self.start_time or
                    time_period.start_time > self.end_time)

    def is_period(self):
        return self.start_time != self.end_time

    def mean_time(self):
        return self.start_time + self.delta() / 2

    def zoom(self, times):
        delta = mult_timedelta(self.delta(), times / 10.0)
        self.start_time += delta
        self.end_time -= delta
        if self.delta() > TimePeriod.MAX_DIFF:
            foo = (self.delta() - TimePeriod.MAX_DIFF) / 2
            self.start_time += foo
            self.end_time -= foo
        elif self.delta() < TimePeriod.MIN_DIFF:
            foo = (TimePeriod.MIN_DIFF - self.delta()) / 2
            self.start_time -= foo
            self.end_time += foo

    def move(self, dir):
        delta = mult_timedelta(self.delta(), dir / 10.0)
        self.start_time += delta
        self.end_time += delta

    def delta(self):
        return self.end_time - self.start_time


def delta_to_microseconds(delta):
    """Convert a timedelta into microseconds."""
    return (delta.days * US_PER_DAY +
            delta.seconds * US_PER_SEC +
            delta.microseconds)


def microseconds_to_delta(microsecs):
    """Convert microseconds into a timedelta."""
    return timedelta(microseconds=microsecs)


def mult_timedelta(td, num):
    """Calculate a new timedelta that is `num` times larger than `td`."""
    days = td.days * num
    seconds = td.seconds * num
    microseconds = td.microseconds * num
    return timedelta(days, seconds, microseconds)


def div_timedeltas(td1, td2):
    """Calculate how many times td2 fit in td1."""
    # Since Python can handle infinitely large numbers, this solution works. It
    # might however not be optimal. If you are clever, you should be able to
    # treat the different parts individually. But this is simple.
    total_us1 = delta_to_microseconds(td1)
    total_us2 = delta_to_microseconds(td2)
    # Make sure that the result is a floating point number
    return total_us1 / float(total_us2)


def time_period_center(time, length):
    """
    TimePeriod factory method.
    
    Create a time period with the given length centered around `time`.
    """
    half_length = mult_timedelta(length, 0.5)
    start_time = time - half_length
    end_time = time + half_length
    return TimePeriod(start_time, end_time)


def get_timeline(input_file):
    """
    Timeline factory method.

    Return a specific timeline depending on the input_file.
    """
    if input_file.endswith(".timeline"):
        from data_file import FileTimeline
        return FileTimeline(input_file)
    else:
        raise Exception("Unknown format")
