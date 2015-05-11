Changelog
=========

Version 1.7.0
-------------

**Planned Release on 30 July 2015.**

Solved problems:

* Crash report: WindowsError: [Error 32] The process cannot access the file because it is being used by another process: 
  (`#33 <https://sourceforge.net/p/thetimelineproj/backlog/33/>`_).  
  
* | It's not possible to see if an event has a hyperlink associated with it, or not.
    (`#29 <https://sourceforge.net/p/thetimelineproj/backlog/29/>`_).  
  | Added an icon displayd in the Event box when the event has hyperlinks.

* | An Event can only have one hyperlink
    (`#30 <https://sourceforge.net/p/thetimelineproj/backlog/30/>`_).  
  | Added support for multiple hyperlinks.
  
* Crash report: TypeError: unsupported operand type(s) for +: 'int' and 'TimeDelta'
  (`#48 <https://sourceforge.net/p/thetimelineproj/backlog/48/>`_).  

* | Show point events as symbols
    (`#42 <https://sourceforge.net/p/thetimelineproj/backlog/42/>`_).  
  | Added an option 'never show paeriod events as point events' to enable period events to be displayed as symbols below the divider line.

* | Lenght of period event is not obvious when zooming out
    (`#46 <https://sourceforge.net/p/thetimelineproj/backlog/46/>`_).     
  | Solved by (`#42 <https://sourceforge.net/p/thetimelineproj/backlog/42/>`_)

* 1.6.0 Crashes on startup
  (`#50 <https://sourceforge.net/p/thetimelineproj/backlog/50/>`_).  

* | Part of sidebar is visible at start of Timeline
    (`#52 <https://sourceforge.net/p/thetimelineproj/backlog/52/>`_).  
  | Made the sidebar hidden at application start-up
  
* | Difficult to troubleshoot errors depending on locale settings
    (`#54 <https://sourceforge.net/p/thetimelineproj/backlog/54/>`_).  
  | Added info on locale settings in the crash report.
  
* | Crash report: AttributeError: 'EraEditorDialog' object has no attribute 'on_return'    
    (`#57 <https://sourceforge.net/p/thetimelineproj/backlog/57/>`_).  
  | Added the on_return attribute to the EraEditorDialog and made it call the controller on_btn_ok method.

* | Crash report: KeyError: '33'
    (`#53 <https://sourceforge.net/p/thetimelineproj/backlog/53/>`_).  
  | Catches the ValueError exception when parsing dates when 'Locale date format' is used.
  
* | Crash report: ValueError: Invalid date.
    (`#55 <https://sourceforge.net/p/thetimelineproj/backlog/55/>`_).    
  | Added better exception handling

* | It is not obvious how to move events vertically
    (`#45 <https://sourceforge.net/p/thetimelineproj/backlog/45/>`_).    
  | Made the Up/Down keys move a selected event vertically.
    That should be more obvious

* | Can't enter dates before 4714 BC
    (`#51 <https://sourceforge.net/p/thetimelineproj/backlog/51/>`_).    
  | Added an experimental feature that allows negative Julian days

Version 1.6.0
-------------

**Released on 30 April 2015.**

Solved problems:

* Dividerline slider pos preserved between sessions

* Introduced a Gradient Event box drawer

* A new Event box drawer is added (gradient draw)

* When selecting period in event editor - end date = start date + 1 day

* Introduced background Era's

* Bitmaps used to mark fuzzy and locked edges

* Fixed crash when opening preferences dialog (wxPython 3.0.2.0)

* Fixed crash when opening hyperlink

* Fixed crash when using experimental feature locale date

* Fixed crash when entering non-ascii characters in feedback dialog subject or text

* Crash report: AttributeError: 'MainFrame' object has no attribute 'open_timeline'
  (`#22 <https://sourceforge.net/p/thetimelineproj/backlog/22>`_).

* Crash report: PyAssertionError: C++ assertion "Assert failure" failed at
  ../src/common/sizer.cpp(1401) in DoInsert(): too many items (9 > 24) in grid
  sizer (maybe you should omit the number of either rows or columns?)
  (`#21 <https://sourceforge.net/p/thetimelineproj/backlog/21>`_).
  This was only a problem with wxPython 3.

* Crash report: KeyError: '33'
  (`#26 <https://sourceforge.net/p/thetimelineproj/backlog/26>`_).
  This happened when using experimental feature 'locale date'.
  
* Added export function timeline -> CSV

* Crash report: ValueError: to_julian_day only works for positive julian days, but was -32104
  (`#43 <https://sourceforge.net/p/thetimelineproj/backlog/43>`_).

Version 1.5.0
-------------

**Released on 31 January 2015.**

New features, enhancements:

* Made progress bar thinner to improve visibility
* Made progress- and done-colors selectable
* Deeper zooming, to one minute, enabled
* Introduced the concept of 'Experimental features'
* Experimental feature - Mark event as done
* Experimental feature - Extend container height
* Experimental feature - Locale date formats

Bug fixes:

* Fixed: Crash report: Duplication subevent
* Fixed: Crash report: Clicking Return in datetimepicker in Event alert editor
* Fixed problem with duplication of containers
* Fixed problem with menus requiring a timeline

Version 1.4.1
-------------

**Released on 12 November 2014.**

Bug fixes:

* Fixed: Crash report: AttributeError: 'MemoryDB' object has no attribute 'events'

Version 1.4.0
-------------

**Released on 9 November 2014.**

New features, enhancements:

* Added undo feature
* Added a context menu to the timeline window
* Added a notification window at the top of the screen when opening a read-only
  timeline or a timeline that is not saved on disk
* Expanded range of numeric time picker
* Added import dialog

Bug fixes:

* Fixed the following error when using wxPython >= 2.9:
  AttributeError: 'module' object has no attribute 'Color'
* Fixed the following error: iCCP: known incorrect sRGB profile
* Fixed navigation problem, go to time, for numeric timeline
* Synchronizing a timeline that has been modified by someone else actually
  reads the modified timeline instead of ignoring it. (This bug was introduced
  in version 1.1.0.)

Version 1.3.0
-------------

**Released on 30 June 2014.**

New features, enhancements:

* Event description included in search target.
* Search result can now be presented and selected in a listbox
* CategoriesEditor is now resizeable

Bug fixes:

* Scrolling with PgUp/PgDn does not crash when it would end up on non-existing
  Feb 29 (`bug report
  <http://sourceforge.net/p/thetimelineproj/mailman/message/32218798/>`_)
* Prevent PyAssertionError when opening category editor (wxPython 3.0.0.0)
* Fit millennium does not crash if timeline is far to the left
* Some Edit menu items are disabled when there is no open Timeline

Version 1.2.4
-------------

**Released on 7 April 2014.**

Bug fixes:

* Exception in event editors when "Add more events after this one" is checked

Version 1.2.3
-------------

**Released on 5 April 2014.**

Bug fixes:

* Shortcuts dissapear when navigation menu is created

Version 1.2.2
-------------

**Released on 5 April 2014.**

Bug fixes:

* Uninitialized flag comes into play when opening an ics file

Version 1.2.1
-------------

**Released on 5 April 2014.**

Bug fixes:

* Encoding problems with navigation menus and shortcut configuration.

Version 1.2.0
-------------

**Released on 5 April 2014.**

New features, enhancements:

* Shortcuts can be user defined.
* Events now have a progress attribute.
* Find feature for categories with Ctrl+F when mouse in category tree.
* Event duration is displayd in the status bar
* Alert dialog appears on top and beeps when shown

Bug fixes:

* Exception when opening event editor from menu for a numeric timeline.
* Incorrect display of decades BC, fixed.
* Contents indicator is drawn even when no balloon data exists.
* End date is set to now in validate function when ends-today is checked

Version 1.1.0
-------------

**Released on 28 December 2013.**

New features, enhancements:

* Century labeling changed. Century 0 is now removed
* Menus for Zoom In and Zoom Out
* Menus for vertical Zoom In and vertical Zoom Out
* Numeric Timeline
* New category tree in sidebar

Bug fixes:

* SVG export can handle ampersand (&) in event text
* SVG export can handle more characters by using UTF-8 encoding
* Prevent overflow error when zooming in on wide events
* Prevent error when using up arrow to increase month in date editor
* Prevent error when fitting all events and they almost fit
* Move event vertically, can be done for events very close to each other (with different y-coordinates)
* Ics-files could load events without text which caused an exception when trying to 'Save As'
* Handle exception in dragging situation when julian day becomes < 0.

Version 1.0.1
-------------

**Released on 4 October 2013.**

Bug fixes:

* Events Disappearing when zooming

Version 1.0.0
-------------

**Released on 30 September 2013.**

After about 4.5 years in development, Timeline 1.0.0 is released. This is the
first time we increment the x-component of the version number
(:ref:`label-version-number`). The main reason for doing so is that Timeline
can no longer read files produced with Timeline versions before 0.10.0
(released over 3 years ago).

The other big thing in 1.0.0 is that the experimental support for dates before
year 0 is no longer experimental. We have rewritten large parts of the date
handling partly to be able to support BC dates in a better way.

New features, enhancements:

* Implemented export to image for whole timeline
* Implemented vertical zooming with Alt+Mousewheel
* Implemented vertical scrolling of timeline events
* Select all, Ctrl-A implemented in event editor description
* New entries in categories tree context menu allowing parent/children
  check/uncheck
* New checkbox under categories tree, used to view categories individually
  independent on parent checked-status
* Dialog for sending feedback (available from help menu and event editor)
* Balloon size restricted to not expand over timeline border
* Help documentation updated
* Show numerical day number together with day name when zooming to week

Bug fixes:

* Fixed exception when right-clicking in CatergoriesEditor
* When 'ends today' start time can't be > now, anymore
* Search bar gives no exception when searching twice or using search button

Removed features:

* Printing: Use export to image and print image instead
* Old Timeline file format: Last used in version 0.9.0

Non-visible changes:

* Adjustments made to be able to use wxPython version 2.9
* Replaced internal time type to support dates before year 0

Version 0.21.1
--------------

**Released on 7 July 2013.**

Bug fixes:

* Bug fix. Exception when exporting image

Version 0.21.0
--------------

**Released on 30 June 2013.**

New features, enhancements:

* Added feature, Set category on selected events
* Added feature, Set category on events without category
* Added 'Import' feature that makes it possible to merge timelines.
* Added 'Edit Event' menu

Bug fixes:

* Bug fix. Allow Preferences setting when no timeline exists
* Bug fix. Reset selected events list when selected events are deleted

Version 0.20.0
--------------

**Released on 30 March 2013.**

New features, enhancements:

* Added 'Save As' feature
* Strategy for allowing multiple users to use the same Timeline file.
* The timeline view regains focus when the event editor is closed.
* Enter-key works in date and time fields of the event editor
* Some help texts updated
* New version of icalender to cope with years before 1900
* TimelineComponent can explicitly clear the drawing area

Bug fixes:

* Fixed problem with Event texts starting with '('- or '['-character
* Delete event by context menu now works

Version 0.19.0
--------------

**Released on 30 December 2012.**

New features, enhancements:

* Possibility to define URL on events and execute "Goto URL" to open web browser.
* Implemented 'fit week' navigation function.
* Help text added, to describe vertical movement of events.

Bug fixes:

* Build script generates zip file with only LF as line endings in files
* Year 0 removed from timeline display when using extended date range

Version 0.18.0
--------------

**Released on 30 September 2012.**

New features, enhancements:

* Zooming with scroll wheel zooms at cursor position instead of center.

Bug fixes:

* Adding multiple events without closing event dialog, works again.
* Alert time comparision problem solved
* Fixed problem with ends-today property
* Fit millennium now works close to edges
* Fit century now works close to edges

Version 0.17.0
--------------

**Released on 15 June 2012.**

This is a new feature release.

New features, enhancements:

* Possibilty to define alerts on events.
* Non-period events can be added to container events

Bug fixes:

* No Error when fitting month, december, when using extended timetype.

Version 0.16.0
--------------

**Released on 31 January 2012.**

This is a new feature release.

New features, enhancements:

* Events can be grouped in containers

Bug fixes:

* Timeline files with non-English names can be opened
* Creating new locked events does not raise exception

Version 0.15.0
--------------

**Released on 30 October 2011.**

This is a new feature release.

New features, enhancements:

* Custom font color for categories
* Measure distance between events
* Only break text in balloon if needed to keep balloon on screen

Bug fixes:

* SVG export can now handle text with non-english characters
* Long category names are now visible in category editor
* Timeline repaints after editing category color
* No year of out range exception in event dialog

Version 0.14.0
--------------

**Released on 30 July 2011.**

This is a new feature release.

New features, enhancements:

* Move all selected events
* Mark event period as fuzzy and edges will change to triangles
* Mark event period as locked and edges will be curved and the event can not
  be moved or resized
* Mark event as ending today and its period will be updated to end today
* Experimental support for inertial scrolling (can be enabled in preferences)
* Shows status text when zooming

Bug fixes:

* Not possible to select too large period when zooming with shift+drag
* Prevent exception (in cases when year was out of range) when scrolling with
  page up/down
* Show user friendly message when creating event with too long period
* Display error message in status bar if period is too long when resizing event
* No time exception when exporting to SVG
* No exception when using extended date range and exporting to SVG

Version 0.13.0
--------------

**Released on 30 April 2011.**

This is a new feature release.

New features, enhancements:

* Events can be moved up and down with Alt+Up/Down
* Hidden event count is shown in status bar
* Event text changes color to white if background is dark
* Timeline can be scrolled with Alt+Left/Right
* Edit category button added in categories editor
* Export to SVG

Bug fixes:

* No exception if "Fit all events" results in a period too large to display
* No error if pressing left or right in empty categories tree control

Version 0.12.1
--------------

**Released on 30 January 2011.**

This is a translation update and bugfix release.

Bug fixes:

* Menu items are correctly disabled if no timeline is open
* Clicking calendar button when an invalid date is entered gives error
  message instead of exception
* LANG environment variable is only set on Windows to prevent locale error at
  startup on Linux systems
* Fit all events ignores hidden events

Version 0.12.0
--------------

**Released on 9 January 2011.**

This is a new feature release.

New features, enhancements:

* Experimental support for extended date range (before 1 AD)

Bug fixes:

* Centuries before 10th are displayed correctly (9 instead of 90)
* Correct translations are used on Windows

New translations:

* Lithuanian
* Vietnamese

Version 0.11.1
--------------

**Released on 24 October 2010.**

This is a translation update and bugfix release.

Bug fixes:

* Create event through menu does not raise exception
* Time removed when saving event and 'Show time' not checked

Version 0.11.0
--------------

**Released on 12 October 2010.**

This is a new feature release.

New features, enhancements:

* New improved date and time entry control
* New navigation function: fit millennium

Bug fixes:

* Remove import of wx.lib.wordwrap that caused a crash on Ubuntu

New translations:

* Italian
* Turkish

Version 0.10.2
--------------

**Released on 11 June 2010.**

This is a translation update and bugfix release.

Bug fixes:

* "Add more events after this one" does not give error message when ticked
  in the create event dialog
* Do not write empty displayed_period tag to xml file
* Prevent application from crashing with wxPython version 2.8.11.0

Version 0.10.1
--------------

**Released on 25 May 2010.**

This is a translation update release.

New translations:

* Polish
* French

Version 0.10.0
--------------

**Released on 9 May 2010.**

This is a new feature release.

New features, enhancements:

* Switch to XML-based file format for storing timeline data
* Support hierarchical categories
* Function to duplicate events according to a pattern
* More user friendly error when application crashes
* Save window position
* More shortcuts for navigation commands
* Selected event gets highlighted line

Bug fixes:

* Application shows error message in category editor instead of crashing

Version 0.9.0
-------------

**Released on 7 February 2010.**

This is a new minor feature and bugfix release.

New features, enhancements:

* Timeline scrolls when creating period events, resizing events, and moving
  events
* Option to start weeks on Sundays
* Balloon shown shorter time after mouse out
* New navigation functions: year, month, week forward/backward
* Middle mouse click centers timeline on that spot
* Shift+Scroll moves horizontal line up/down

Bug fixes:

* Fixed issues with 'Go to Date' dialog
* Balloon now visible even if event stretches outside screen
* All keys now work in the search bar
* Prevent crash if long period events are used
* Small corrections to documentation

Version 0.8.0
-------------

**Released on 1 January 2010.**

This is a new minor feature release.

New features, enhancements:

* Basic search function
* Weekend day numbers are drawn in bold in month view
* Experimental read-only support for ics files
* Timeline that shows last modified dates of files in a directory
* Allow balloons to stick
* Write files in a safer way without permanent backups
* New navigation functions: find first, find last, fit century, fit decade,
  fit all
* New icons in help browser (Windows)
* Man page (GNU/Linux)

Bug fixes:

* Fit month and fit day now work for December and last day of month
* The same help page can now be opened again after the help browser is closed
* Recently opened list can't contain the same file twice now

New translations:

* Hebrew (Yaron Shahrabani)
* Catalan (BennyBeat)

Version 0.7.0
-------------

**Released on 1 December 2009.**

This is a new minor feature release.

New features, enhancements:

* Visual move and resize of events
* Snap when creating, moving, and resizing events
* Show balloons with event information on hover
* Associate icons with events (shown in balloons)
* Improved drawing of events: new selection and data indicator
* Added context menu for events

New translations:

* Russian (Sergey Sedov)

Version 0.6.0
-------------

**Released on 1 November 2009.**

This is a new minor feature release.

New features, enhancements:

* Added shortcuts for editing categories from the event editor dialog
* Mapped backspace key to previous page in help browser
* Added option to open most recent timeline at startup (default yes)
* Show exact time of an event in status bar
* The y position of the divider between period events and single point
  events can now be adjusted

Bug fixes:

* Period events with description now has correct width
* The legend is now always drawn on top of events

Version 0.5.0
-------------

**Released on 1 October 2009.**

This is a new feature release.

New features, enhancements:

* Added 'Open Recent' menu
* Replaced manual with a wiki-like help system
* Visualize description of selected events in balloons
* Improved error messages when reading or writing timeline data fails
* Added functionality for printing timeline
* Added new navigation functions: Backward/Forward
* Added welcome panel that shows if no timeline is open

New translations:

* Dutch (Koert Loret)

Bug fixes:

* Fixed problem on Windows where you could not enter dates before 1752-09-14

Version 0.4.0
-------------

**Released on 1 September 2009.**

This is a new feature release.

The first step in supporting additional data for events has been implemented.
The file format had to be changed for this. Files written by version 0.4.0 will
not be readable by previous versions, but 0.4.0 can read 0.3.0 files and will
convert them automatically.

New features, enhancements:

* Translation support
* Export to Image
* Legend for categories
* Longer descriptions for events (visualization will be implemented in 0.5.0)

New translations:

* Swedish (Roger Lindberg)
* Spanish (Roman Gelbort)
* German (Nils Steinger)
* Brazilian Portuguese (Leonardo Frigo da Purificação)

Version 0.3.0
-------------

**Released on 1 August 2009.**

In this release the documentation has been improved and a few bugs have been
fixed.

The file format has also been updated to decrease the risk of loosing data.
Users are therefore strongly encouraged to upgrade to this version. The file
format is readable by the 0.2.0 version but it can not take advantage of the
new format.

New features, enhancements:

* Changed to allow events without categories.
* Improved what's displayed in the title bar (open file name first).
* Added application icon.
* Added Help menu.
* Converted user manual to DocBook format.
* Integrated user manual with application (first step).
* Started experimenting with unit tests.
* Added copyright notes to all source files.
* Added AUTHORS, CHANGES, COPYING, and INSTALL.

Bug fixes:

* Fixed bug where application raised exceptions when scrolling to the very
  end or the very beginning of time (year 10 or year 9999).
* If multiple timelines were opened, the displayed period would just be saved
  for the last opened one. That is fixed now so it is saved for all.

Version 0.2.0
-------------

**Released on 5 July 2009.**

This version contains lots of improvements.

File format written by this version is not readable by previous versions.

New features, enhancements:

* Added support for showing and hiding events from certain categories.
* Added a week view in one zoom level of the timeline.
* Added navigation functions such as 'Go to Date' and 'Go to Today'.
* Improved controls for entering a date and time.

Version 0.1.0
-------------

**Released on 11 April 2009.**

First usable version.

.. _label-version-number:

A note about version numbers
----------------------------

Timeline uses a three-component version numbering system (X.Y.Z).

Z is only incremented when critical bugs are corrected or translations are
updated. The functionality of the program is the same for all X.Y versions.

Y is incremented every time a new feature or enhancement is added.

X is incremented when the new version is no longer compatible with previous
versions or when the program undergoes some big change or significant
milestone.
