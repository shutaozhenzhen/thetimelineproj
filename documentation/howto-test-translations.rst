Run Timeline in a different language
====================================

First you need to compile the translation files::

    python3 tools/generate-mo-files.py

It requires the ``msgfmt`` program to be on the path. See :ref:`label-gettext`
for instructions how to install it.

Then you need to change your locale before running Timeline. On a Linux system,
you can do it like this::

    LANG=sv_SE python3 source/timeline.py
