"""
Program main entry point.

Responsible for processing command line options and initializing the
application.
"""


from sys import argv
from optparse import OptionParser
import logging
from logging import info as loginfo

import wx

from gui import MainFrame
from version import get_version


def parse_options():
    version_str = "%prog " + get_version()
    op = OptionParser(usage="%prog [options] [filename]", version=version_str)
    op.add_option("-l", "--log-level", type="int", default=logging.ERROR,
                  help="specify log level (0 to log everything)")
    op.add_option("-f", "--log-file", default=None,
                  help="specify a file to send log messages to")
    # Skip first command line argument since it is the name of the program
    return op.parse_args(argv[1:])


def setup_logging(level, file):
    format= "%(asctime)s [%(levelname)s] %(message)s"
    # Setup logging to stderror
    console_hanler = logging.StreamHandler()
    console_hanler.setFormatter(logging.Formatter(format))
    console_hanler.setLevel(level)
    logging.getLogger().addHandler(console_hanler)
    # Setup logging to file
    if file:
        file_handler = logging.FileHandler(file, "w")
        file_handler.setFormatter(logging.Formatter(format))
        file_handler.setLevel(level)
        logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(level)
    loginfo("Logging set up with level=%s, file=%s", level, file)


def create_wx_app(input_files):
    app = wx.PySimpleApp()
    main_frame = MainFrame()
    main_frame.Show()
    for input_file in input_files:
        main_frame.open_timeline(input_file)
    return app


def main():
    (options, input_files) = parse_options()
    setup_logging(options.log_level, options.log_file)
    app = create_wx_app(input_files)
    app.MainLoop()


if __name__ == '__main__':
    main()
