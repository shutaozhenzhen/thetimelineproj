"""
Custom data types.
"""


from logging import warning as logwarning

from data_file import FileTimeline
from data_file2 import FileTimeline2
from data_dummy import DummyTimeline


def get_timeline(input_file):
    """
    Timeline factory method.

    Return a specific timeline depending on the input_file.
    """
    if input_file == "dummy":
        return DummyTimeline()
    elif input_file.endswith(".timeline2"):
        return FileTimeline2(input_file)
    elif input_file.endswith(".timeline"):
        return FileTimeline(input_file)
    else:
        logwarning("Unable to open timeline '%s', unknown format", input_file)
        return None
