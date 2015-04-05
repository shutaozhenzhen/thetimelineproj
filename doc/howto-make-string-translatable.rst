Make a string translatable
==========================

If you introduce a new string in the source code that you would like to be
translated into different languages, you need to do 2 things:

1. Enclose the string in ``_()``
2. Upload a pot file to :ref:`Launchpad <label-launchpad>`

Example of enclosed string::

    print(_("Hello!"))

To generate a pot file, run ::

    ./po/generate-pot-file.py

It requires the ``xgettext`` program to be on the path. See :ref:`label-gettext`
for instructions how to install it.

You should now have a file ::

    ./po/timeline.pot

that contains an entry for your string looking something like this::

    #: source/timeline.py:58
    msgid "Hello!"
    msgstr ""

Upload this pot file to Launchpad. Then translators will see your new string
and can translate it.
