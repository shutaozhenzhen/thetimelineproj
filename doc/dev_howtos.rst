Howto's
=======

.. _howto-doc-html:

Generate the documentation in HTML format
-----------------------------------------

Make sure that you have all required :ref:`tools <tools>` installed.

The root directory for all the documentation is "doc" and there you will find a
*Makefile* with instructions how to generate the documentation in various
formats.

If you have *Make* installed, you can issue the command ``make html`` on Linux
or ``make htmlw`` on Windows to generate the documentation in HTML format. The
index page will be output in "doc/_build/html/index.html"

Use logging
-----------

To print log messages from the code, first import the ``logging`` module, and
then use one of the logging functions like this::

    import logging
    logging.critical("Error in drawing", exc_info=e)
    logging.error("foo not of correct type %s", foo)
    logging.warning("")
    logging.info("")
    logging.debug("")

For more information on logging, read http://www.python.org/doc/2.5.2/lib/module-logging.html.
