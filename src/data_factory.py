"""
Custom data types.
"""


import logging

from datetime import datetime as dt

from data_file import FileTimeline
from data_dummy import DummyTimeline


def get_timeline(input_files):
    """
    Timeline factory method.

    Return a specific timeline depending on the input_files.
    """
    if len(input_files) == 1 and input_files[0] == "dummy":
        return DummyTimeline()
    elif len(input_files) == 1:
        return FileTimeline(input_files[0])
    else:
        logging.warning("Unable to open timeline for %s, unknown format", input_files)
        return None



