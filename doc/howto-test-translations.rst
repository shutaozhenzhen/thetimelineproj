Test translations
=================

First you need to compile the translation files::

    ./po/generate-mo-files.py

It requires the ``msgfmt`` program to be on the path. See :ref:`label-gettext`
for instructions how to install it.

Then you need to change your locale before running Timeline. On a Linux system,
you can do it like this::

    LANG=sv_SE ./source/timeline.py
