
Analysis of Timeline emails (2015-06)
=====================================

This article was written using `Ipython
Notebook <http://ipython.org/>`__.

First we import all modules that we will use:

.. code:: python

    %matplotlib inline
    import mailbox
    import email.utils
    import matplotlib.pyplot as plt
    import subprocess
    import sys
    import re

Paths that you might need to change if you want to reproduce this
document yourself:

.. code:: python

    PATH_TO_MALING_LIST_EXPORT = "thetimelineproj-user"
    PATH_TO_REPO = "main-sf"

For reference, this is the Python version:

.. code:: python

    sys.version




.. parsed-literal::

    '2.7.6 (default, Mar 22 2014, 22:59:56) \n[GCC 4.8.2]'



An iterator for emails
----------------------

I downloaded all emails from SourceForge. (You need to be project admin
to do that.) It came in mbox format. We can work with it in Python like
this:

.. code:: python

    def email_iterator():
        for message in mailbox.mbox(PATH_TO_MALING_LIST_EXPORT):
            yield Message(message)
    
    class Message(object):
        
        def __init__(self, message):
            date = email.utils.parsedate_tz(message["date"])
            self.month_tuple = (date[0], date[1])
            self.subject = message.get("subject", "")

Let's see if we can get the title of the first email:

.. code:: python

    email_iterator().next().subject




.. parsed-literal::

    '[Thetimelineproj-user] Test'



And count them all:

.. code:: python

    len(list(email_iterator()))




.. parsed-literal::

    2126



Email frequency
---------------

The first question I would like to answer is how email frequency looks
like over time. Let's extract some data:

.. code:: python

    emails_per_month = {}
    for message in email_iterator():
        emails_per_month[message.month_tuple] = emails_per_month.get(message.month_tuple, 0) + 1

Let's see if we got that right. What are the first 5 keys?

.. code:: python

    sorted(emails_per_month.keys())[:5]




.. parsed-literal::

    [(2009, 6), (2009, 7), (2009, 8), (2009, 9), (2009, 10)]



Looks right. What about frequencies?

.. code:: python

    emails_per_month[(2009, 6)]




.. parsed-literal::

    2



.. code:: python

    emails_per_month[(2009, 7)]




.. parsed-literal::

    12



Looks good too. And how many emails have we got in total?

.. code:: python

    sum(emails_per_month.values())




.. parsed-literal::

    2126



Next we would like to plot this data. Here are some functions for that:

.. code:: python

    def plot_frequencies_per_month(frequencies_per_month):
        (x, xlabels, y) = ([], [], [])
        
        index = 0
        for year in range(2009, 2016):
            for month in range(1, 13):
                x.append(index)
                xlabels.append("%d-%02d" % (year, month))
                y.append(frequencies_per_month.get((year, month), 0))
                index += 1
    
        plt.figure(figsize=(15, 5))
        plt.bar(x, y, align="center", color=(0.8, 0.8, 1))
        plt.xticks(x, xlabels, rotation=90)
    
        plot_moving_average(x, y, 6, "r")
        plot_moving_average(x, y, 12, "g")
        plot_moving_average(x, y, 24, (0, 0, 0))
    
        plt.legend()
        plt.tight_layout()
        plt.axis("tight")
        plt.grid(axis="y")
        
    def plot_moving_average(x, y, period_length, color):
        averages = []
        for _ in range(period_length-1):
            averages.append(0)
        for index in range(len(y)-period_length+1):
            averages.append(sum(y[index:index+period_length]) / period_length)
        plt.plot(x, averages, color=color, linewidth=2, label="%d months moving average" % period_length)

And the result is this:

.. code:: python

    plot_frequencies_per_month(emails_per_month)
    plt.title("Number of emails per month")
    plt.show()



.. image:: analysis_timeline_emails_output_24_0.png


The email frequency seems pretty constant until around 2013-08. What
happened then? On 30 September 2013 version 1.0.0 was released. The peak
at 2013-10 is right after the 1.0.0 release. Does it mean that users are
afraid to use software where the version number is < 1.0 because it
feels unstable?

On the other hand, what does email frequncy mean? Let's have a look at
the emails from 2013-10.

.. code:: python

    peak_emails = []
    for message in email_iterator():
        if message.month_tuple == (2013, 10):
            peak_emails.append(message)

From the diagram, the number of peak emails should be a little over 140.
Does it match?

.. code:: python

    len(peak_emails)




.. parsed-literal::

    150



Let's look at the titles:

.. code:: python

    for subject in sorted(set(message.subject for message in peak_emails)):
        print(subject)


.. parsed-literal::

    1 of 3 Event Hides or Disappears Upon Zoom-In
    =?UTF-8?Q?SV:_Crash_report:_OverflowError:_l?=
    	=?UTF-8?Q?ong_int_too_large_to_convert_to_int=E2=80=8F?=
    =?windows-1256?Q?Crash_repo?= =?windows-1256?Q?rt:_Overfl?=
    	=?windows-1256?Q?owError:_l?= =?windows-1256?Q?ong_int_to?=
    	=?windows-1256?Q?o_large_to?= =?windows-1256?Q?_convert_t?=
    	=?windows-1256?Q?o_int=FE?=
    Ampersand breaks svg export
    Bug report + suggestion .................and a supplicate
    Can containers be nested?
    Category Uncheck "stickyness"
    Coding standards
    Crash report: AttributeError: 'NoneType' object has no attribute
    	'path'
    Crash report: AttributeError: 'tuple' object has no attribute 'year'
    Crash report: OverflowError: long int too large to convert to int
    Feedback
    Feedback + an addition
    Feedback on event editor dialog
    File Notification from brian@genalchemy.com: TLP-1.0-Problem.zip
    Installing from source in Android?
    Keyboard Shortcuts
    Loss of Period Events Created in 2.1 Series Timeline
    New category tree 
    Numeric timeline
    Period Stability Bug in v 1.0
    Re: 1 of 3 Event Hides or Disappears Upon Zoom-In
    Re: Ampersand breaks svg export
    Re: Bug report + suggestion .................and a supplicate
    Re: Can containers be nested?
    Re: Category Uncheck "stickyness"
    Re: Coding standards
    Re: Crash report: AttributeError: 'NoneType' object has no
    	attribute'path'
    Re: Crash report: AttributeError: 'NoneType' object has no attribute
    	'path'
    Re: Crash report: AttributeError: 'tuple' object has no attribute
    	'year'
    Re: Crash report: OverflowError: long int too large to convert to int
    Re: Crash report: PyAssertionError: C++ assertion
    	"win->GetBackgroundStyle() == wxBG_STYLE_CUSTOM" failed at
    	c:\BUILD\wxPython-src-2.8.11.0\include\wx/dcbuffer.h(251)
    	in wxAutoBufferedPaintDC::TestWinStyle(): In constructor,
    	you need to call SetBackgroundStyl
    Re: Feedback
    Re: Feedback + an addition
    Re: Feedback on event editor dialog
    Re: Installing from source in Android?
    Re: Keyboard Shortcuts
    Re: Loss of Period Events Created in 2.1 Series Timeline
    Re: New category tree
    Re: Numeric timeline
    Re: Period Stability Bug in v 1.0
    Re: Release annonuncer
    Re: SV: Coding standards
    Re: Saving a readable whole chronology image + svg export bug
    Re: The announcer
    Re: Updates
    Re: Zooming
    Re: import data for a time line from Excel??
    Re: possible typo in
    	timelinelib/wxgui/component.py::DummyConfig.__init__()
    Re: svg image export
    Re: thetimelineproj-user Digest, Vol 51, Issue 12
    Re: thetimelineproj-user Digest, Vol 51, Issue 2
    Re: thetimelineproj-user Digest, Vol 51, Issue 3
    Release annonuncer
    SV: 1 of 3 Event Hides or Disappears Upon Zoom-In
    SV: Bug report + suggestion .................and a supplicate
    SV: Can containers be nested?
    SV: Coding standards
    SV: Crash report: AttributeError: 'NoneType' object has no
    	attribute	'path'
    SV: Crash report: AttributeError: 'NoneType' object has no
    	attribute'path'
    SV: FW: Disappearing Period Events....
    SV: Keyboard Shortcuts
    SV: Loss of Period Events Created in 2.1 Series Timeline
    SV: New category tree
    SV: RE: SV: Crash report: OverflowError: long int too large to
    	convert to int?
    SV: Release annonuncer
    SV: SV: Coding standards
    SV: String Index Out of Range
    SV: The announcer
    SV: Two Questions: Cmd-line and seconds
    SV: thetimelineproj-user Digest, Vol 51, Issue 2
    Saving a readable whole chronology image + svg export bug
    String Index Out of Range
    The announcer
    Two Questions: Cmd-line and seconds
    Updates
    Zooming
    import data for a time line from Excel??
    possible typo in
    	timelinelib/wxgui/component.py::DummyConfig.__init__()
    small suggestion
    svg image export


Not sure if this says anything.

Crash report frequency
----------------------

Now let's do the same frequency analysis but only include crash report
emails. They were introduced later in Timeline and therefore we should
not see such reports early on.

.. code:: python

    crash_reports_per_month = {}
    for message in email_iterator():
        if "Crash report" in message.subject:
            crash_reports_per_month[message.month_tuple] = crash_reports_per_month.get(message.month_tuple, 0) + 1
            
    plot_frequencies_per_month(crash_reports_per_month)
    plt.title("Number of crash reports per month")
    plt.show()



.. image:: analysis_timeline_emails_output_33_0.png


It's a little harder to see a trend here becuase of lack of data early
on. But it looks like there is a slight increase around 2015-02. What
happened then? Nothing in particular from the changelog.

Commit frequency
----------------

It would be interesting to look at the repo history. What are the number
of commits each month? Does that affect the number of emails or crash
reports each month?

We can extract the frequencies of commits per month like this:

.. code:: python

    output = subprocess.check_output([
        "hg", "log",
        "--template", "{date|isodate}\n"
    ], cwd=PATH_TO_REPO)
    
    commits_per_month = {}
    
    for line in output.strip().split("\n"):
        match = re.match(r"(\d{4})-(\d{2})", line)
        month_tuple = (int(match.group(1)), int(match.group(2)))
        commits_per_month[month_tuple] = commits_per_month.get(month_tuple, 0) + 1

The plot:

.. code:: python

    plot_frequencies_per_month(commits_per_month)
    plt.title("Number of commits per month")
    plt.show()



.. image:: analysis_timeline_emails_output_38_0.png


There is a peak of commits around 2014-09.

To see how data correlates it would be better to have the time period be
releases instead of months. That way we can more easily see how the
frequencies of emails and commits varies between releases of Timeline.
Maybe the next analysis article?
