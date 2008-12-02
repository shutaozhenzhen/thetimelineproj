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

Handle EOL characters in files
------------------------------

For all new text files added to the SVN repository, the following command
should be issued to ensure that that native EOL style is used when the file is
checked out::

    svn propset svn:eol-style native [new_file]

This will greatly simplify working on different platforms that uses different
EOL styles (LF on Linux, CRLF on Windows).

To simplify this, one could use so called automatic properties. This is
configured in the Subversion client. On Unix machines the path to the
configuration file is ``~/.subversion/config``, and on Windows
``%APPDATA%\Subversion\config``. Automatic properties is configured as
follows::

    [miscellany]
    enable-auto-props = yes

    [auto-props]
    README = svn:eol-style=native
    Makefile = svn:eol-style=native
    *.py = svn:eol-style=native
    *.rst = svn:eol-style=native

Add one line for each type of file that you might create.
