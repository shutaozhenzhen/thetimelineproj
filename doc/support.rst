Support
=======

Do you need help with Timeline? Do you want to help others with Timeline? This
is where to look.

Documentation
-------------

The documentation you are reading right now might have the answer to your
question. Browse it to see if you can find it. You can also search it by typing
in a search term in the "Quick search" field in sidebar to the left.

Mailing list
------------

We use a :ref:`mailing list <label-mailing-list>` for all kinds of discussions
about Timeline. If you have a question about Timeline, you can send it to the
mailing list. Everyone that is registered will receive your message and can
write a response.

Before you send your question, please browse or search the mailing list archive
to see if you can find your answer.

If you want to participate in the discussions on the mailing list and help
answer users' questions about Timeline, you need to register.

FAQ
---

Can't zoom wider than 1200 years
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*This workaround should not be needed in versions > 1.7.0.*

Timeline should not be able to zoom wider than 1200 years. But unfortunately,
this happens sometimes, and a period larger than 1200 years gets written to the
``.timeline`` file.

When this happens, you can no longer open the file.

This is a bug in Timeline that we should fix. But there is a workaround that
you can use to fix the problem yourself.

The ``.timeline`` file is actually just an xml file. In there, somewhere around
the bottom of the file, you should find this section::

    <displayed_period>
      <start>2013-09-28 00:10:06</start>
      <end>2013-10-09 20:34:55</end>
    </displayed_period>

If you open the ``.timeline`` file in a text editor and change the start and
end dates to be a period less than 1200 years, you should be able to open your
file again.

Make sure that you save the file with UTF-8 encoding.

Standard email responses
------------------------

Here are some standard email responses to common emails on the mailing list.
Use them as a template when answering questions on the mailing list.

Crash report that has not been fixed::

    Thanks for taking the time to report this error.

    We have added the problem to our backlog:
    https://sourceforge.net/p/thetimelineproj/backlog/

    /The Timeline Team

Crash report that has been fixed in the upcoming release::

    Thanks for taking the time to report this error.

    The problem has been fixed and will be available in the next release.

    /The Timeline Team

Crash report that has been fixed in released version::

    Thanks for taking the time to report this error.

    The problem has been fixed in the current version. It can be downloaded
    here: https://sourceforge.net/projects/thetimelineproj

    /The Timeline Team

Person interested in developing Timeline::

    We're glad you're interested in contributing to Timeline. We want to help
    as much as we can.

    Here are some points you can start with:

    * We have a backlog of problems that we want to solve
      (https://sourceforge.net/p/thetimelineproj/backlog)

    * Crash reports in the backlog are usually easy to fix. Although they might
      require some investigation.

    * Timeline is licensed under GLPv3. We propose a model where you (and
      everyone else) keep the copyright of their patches. As the patches will
      be GPLv3 as well, we can include them in the project.

    * Registering on this mailing list is a good idea.

    * The website has some more information:
      http://thetimelineproj.sourceforge.net/

    * Some sections about developing are outdated.

    * We're here on the mailing list to help you with any questions you have :-)

    /The Timeline Team
