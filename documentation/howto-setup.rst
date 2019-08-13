Setting up a development environment
====================================

Timeline uses the `Mercurial <http://mercurial.selenic.com>`_ version control
system. You can clone the repository with the following command::

    hg clone http://hg.code.sf.net/p/thetimelineproj/main

Once you have the repository cloned, you need to install dependencies (see
:ref:`label-installing-dependencies`) and development tools (see the next
section).

Then make sure you can run all tests::

    python3 tools/execute-specs.py

If that works, you have the basic environment set up.

Installing development tools
----------------------------

This section describes how to install developments tools. Some tools are only
needed in certain situations.

mock (Python package)
^^^^^^^^^^^^^^^^^^^^^

http://pypi.python.org/pypi/mock

This is used in some tests.

At the moment, this is included in the Timeline repository and does not have to
be installed.

.. _label-gettext:

gettext
^^^^^^^

http://www.gnu.org/software/gettext/

This is used when working with translations. It is also used when running
tests.

Windows users: get the zipfiles gettext-tools-0.17.zip and
gettext-runtime-0.17-1.zip from here
http://ftp.acc.umu.se/pub/gnome/binaries/win32/dependencies/.
