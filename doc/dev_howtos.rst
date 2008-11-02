How-to's
========

Generate the documentation in HTML format
-----------------------------------------

`Sphinx <http://sphinx.pocoo.org>`_ is used to generate the documentation in
HTML format. Make sure that it is installed before proceeding.

The root directory for all the documentation is "doc" and there you will find a
*Makefile* with instructions how to generate the documentation in various
formats.

If you have *Make* installed, you can issue the command ``make html`` on Linux
or ``make htmlw`` on Windows to generate the documentation in HTML format. The
index page will be output in "doc/_build/html/index.html"
