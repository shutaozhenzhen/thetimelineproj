Installling
===========

Timeline runs on multiple platforms. If you can run `Python
<http://www.python.org/>`_ and `wxPython <http://www.wxpython.org/>`_ you
should be able to run Timeline.

The recommended way to install Timeline is with a binary package or installer.
If that is not available for your platform, you have to install from source.

If you have problems installing Timeline, please see the :doc:`support` page
for ways to get help.

Windows
-------

.. image:: /images/logo-windows.png
    :align: right

We provide a binary installer for Windows. It installs an executable version of
Timeline that is self contained and doesn't need any other dependencies.

Download one of the following installers:

* Latest release: |latest_exe|_
* Beta version: `latest Windows build <https://jenkins.rickardlindberg.me/job/timeline-windows-exe/lastSuccessfulBuild/artifact/>`_

The beta version is for users that want to try the latest features and give
feedback on them before a release.

Fedora
------

.. image:: /images/logo-fedora.png
    :align: right

Timeline exists in the Fedora repositories. Install it with the following
command::

    sudo dnf install timeline

The version included in Fedora is often not the latest. If you want the latest
version, you have to install from source.

Installing from Snapcraft
-------------------------

https://snapcraft.io/timeline

Installing from source
----------------------

.. image:: /images/logo-source.png
    :align: right

Download one of the following source packages:

* Latest release: |latest_zip|_
* Beta version: `latest source build <https://jenkins.rickardlindberg.me/job/timeline-linux-source/lastSuccessfulBuild/artifact/>`_

The beta version is for users that want to try the latest features and give
feedback on them before a release.

When you install from source, you have to install required dependencies
yourself. See the next section for instructions how to do that. Once that is
done, and you have extracted the zip file, you should be able to run Timeline
with this command::

    python <path-to-timeline-directory>/source/timeline.py

.. HINT::

    If you get an error similar to the one bellow, there is probably a
    dependency missing::

        $ python source/timeline.py
        Traceback (most recent call last):
          File "source/timeline.py", line 64, in <module>
            setup_humblewx()
          File "source/timelinelib/wxgui/setup.py", line 35, in setup_humblewx
            import humblewx
        ImportError: No module named humblewx

.. _label-installing-dependencies:

Installing dependencies
^^^^^^^^^^^^^^^^^^^^^^^

This section describes how to install the software that Timeline depends on.

Python
######

http://www.python.org

There is most definitely a binary package or installer for your platform.

Timeline requires version 2.6 or greater.

wxPython (Python package)
#########################

http://www.wxpython.org

There is probably a binary package or installer for your platform.

Timeline requires version 3.0 or greater.

humblewx (Python package)
#########################

https://github.com/thetimelineproj/humblewx

A Python package that we extracted from the Timeline source code because it
could be generally useful.

The latest version can be installed with the following command::

    pip install --user git+https://github.com/thetimelineproj/humblewx.git

icalendar (Python package)
##########################

http://pypi.python.org/pypi/icalendar

At the moment, this is included in the Timeline repository and does not have to
be installed.

markdown (Python package)
#########################

http://pypi.python.org/pypi/Markdown

At the moment, this is included in the Timeline repository and does not have to
be installed.

pysvg (Python package)
######################

http://code.google.com/p/pysvg/downloads/list

At the moment, this is included in the Timeline repository and does not have to
be installed.
