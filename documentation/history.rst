Project history
===============

Initial mission statement
-------------------------

In the very beginning, Timeline was created because Rickard was frustrated with
regular calendars. He found it difficult to get a sense of when events occurred
in time. Especially events far apart that would not fit in a calendar view. He
thought that presenting events on a timeline where he could quickly zoom in and
out and move around to show different views would help.

So, the core task of Timeline is to **display and navigate events on a
timeline**. It has done that since version 0.1.0 which was released on 11 April
2009. Excerpt from the README:

    The Timeline Project aims to create a cross-platform application for
    displaying and navigating information on a timeline. The main goal is that
    it should be easy to quickly display different periods in time with
    different kinds of information on the timeline.

If you have data that you would like to display on a timeline, Timeline should
be able to show it. Timeline has multiple backends to display data from
different sources.

Conference 2015
---------------

The first Timeline conference took place at Södertuna castle on the 13-15
February 2015.

The Timeline team met to discuss future directions of the project.

.. figure:: /images/2015-conference-castle.jpg

    Södertuna castle.

.. figure:: /images/2015-conference-team.jpg

    The Timeline team.

Summary:

* We want to continue developing Timeline
* We want to get more people involved in the development of Timeline
* We worked on making it easier for new people to get into Timeline

    * We started writing guides
    * We improved the structure of the files in the repository
    * We experimented with a plugin architecture that will make it easier to
      make small modifications to Timeline

* We want to let the Timeline community decide the direction in which Timeline
  should develop

    * We looked at mailing list traffic from 2014 to learn what problems users
      face when they are using Timeline
    * We started entering those problems in a backlog
    * We documented the process we should try to follow
    * In this process, all users' problems are entered in the backlog
    * We try to solve problems from the backlog that most users have faced

Conference 2016
---------------

The second Timeline conference took place at Trosa stadshotell on the 12-14
February 2016.

Review of past year:

* We have continued to develop Timeline. We are happy with that and will
  continue.
* More people are involved in discussions about Timeline. We are happy about
  that. Although there have been no contributions of code.

We discussed if extracting the canvas component would be a good project to work
on. Reasons for doing it:

* More developers might contribute code to the canvas component if they use it
  themselves in their own project.
* The canvas is used today but is not supported by us.

We discussed having a forum instead of the mailing list and backlog. Problems
it might solve:

* The discussion happens in one place: in the forum thread instead of first on
  the mailing list and then transfered to the backlog.
* It is easier to see the history of discussions compared to the mailing list
  archive.

Refactoring goals:

* Rename timeline to db.
* Move test/specs to test/unit and test/something-else.
