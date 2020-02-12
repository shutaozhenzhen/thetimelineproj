Changelog
=========

Version 2.2.0
--------------

**Planned to be Released on 3 May 2020.**

*Don't want to wait for the final release? Try the beta version!*

* `Download source <https://jenkins.rickardlindberg.me/job/timeline-linux-source/lastSuccessfulBuild/artifact>`_.

* `Download windows installer <https://jenkins.rickardlindberg.me/job/timeline-windows-exe/lastSuccessfulBuild/artifact/tools/winbuildtools/inno/out/>`_.

Event filtering:

* ``Now Events can have labels on which visibility filtering is possible.``
  The sidebar can show label filter component and labels can be defined for an Event.


Fixed crash reports and bugs:

* ``A MenuItem ID of Zero does not work under Mac.``
  Starting with MenuItem ID = 1

* ``ValueError: julian_day must be >= 0.``
  Added an exception check when zooming to avoid exception.

* ``User date format has dissapeared.``
  Made the user date format come into play again.

* ``AttributeError: 'StripDay' object has no attribute 'appearance'.``
  Added appearance to StripDay in In Pharanic time type.

* ``AttributeError: 'PharaonicTimeType' object has no attribute 'get_day_of_week'.``
  Removed 'week'-logic from StripDay().

Version 2.1.0
--------------

**Released on 25 January 2020.**

New Dialogs:

* ``Measure duration of events.``
  A new dialog has been built for calculating duration of events.

* ``Users has asked for a better way of finding a milestone.``
  A new dialog has been built for navigating to a milestone.

System info:

* ``Python encoding is missing in system info dialog.``
  Python encoding name added to in system info dialog.

Fixed crash reports and bugs:

* ``invalid index in wxListBox::SetSelection.``
  Showing Message Box when there are no milestones found

* ``'Image' object has no attribute 'SaveStream'.``
  Changed functions for coding/decoding icon images.

* ``AttributeError: 'MainCanvas' object has no attribute 'controller'.``
  Added controller property to MainCanvas.

* ``TypeError: invalid result from FileDropTarget.OnDropFiles(), an integer is required (got type NoneType).``
  Changed logic in OnDropFiles to fullfill he api.

* ``error : a "calendar.bmp" file is missing.``
  Using calendar.png instead.

* ``UnicodeDecodeError: 'gbk' codec can't decode byte 0x93 in position 3750: Illegal multibyte sequence.``
  Using utf-8 encoding when reading first line in timeline file.

* ``AttributeError: module 'time' has no attribute 'clock'.``
  The tim.clock() function is now replaced with the time.process_time() function.

Version 2.0.0
--------------

**Released on 3 November 2019.**

Port of Timeline to Python 3.

Removed features:

* The main menu is no longer available as a context menu.

Eras:

* ``Tha application don't start if the timeline has Era's with no duration.``
  Removed Era's with no duration from drawing.


Version 1.20.0
--------------

**Released on 3 November 2019.**

Versions:

This is the last release in the 1.x version series.
The application has bas been ported to Python 3 and releases will continue
in the 2.0 version.

Calendars:

* ``Two new calendars added.``
  The Pharaonic and Coptic calendars added, thanks to Guyrandy Jean-Gilles.

Time:

* ``The time for an event can be entered with seconds precision.``
  A preference can be checked in the date/time tab to make the time-picker show seconds.

Graphics:

* ``The font in the event description editor has a fixed size.``
  When the text control has focus the font size can be changed with Ctrl+/Ctrl-.

* ``The with of the now-line can be 2 pix wider to help old eyes.``
  A preference can be checked in the color tab to make the now-line wider.

Search:

* ``When only one event is found, pressing Enter has no effect.``
  On Enter, if we are on the last event found, the first event found is highlighted.

* ``Period selection is added to the Search control.``
  The search period can be limited to the visible time period.

* ``Result label is always shown.``
  Now the result label is shown even when more than 1 match.

Fixed crash reports and bugs:

* ``AttributeError: 'MainCanvas' object has no attribute 'controller'``
Fixed controller that had changed name crom _controller.

* ``AttributeError: 'NumTime' object has no attribute 'julian_day'``
  Added to_str() function to time base class GenericTimeMixin.
  Own implementation of to_str in GregorianTime.

* ``AttributeError: 'NoneType' object has no attribute 'get_time_period'``
  Removed None objects from event list.

* ``AttributeError: 'NoneType' object has no attribute 'delete'``
  Removed None objects from event list.

* ``TypeError: MessageDialog(): argument 1 has unexpected type'SvgExporter'.``
  Fixed window reference.

Version 1.19.0
--------------

**Released on 30 April 2019.**

Time scale position:

* ``The position of the time scale can be changed with a preference value.``
  The position can be at top, at bottom or at the center line.

Default Dates:

* ``For Gregorian dates, default values for year, month and day can be used in input fields.``
  The feature can be selected with a preference setting.

Export:

* ``Not all events are shown in export listbox when filtering is turned off.``
  Include events without category when filtering is turned off.

Fixed crash reports and bugs:

Moving event vertically:
* ``AttributeError: 'NoneType' object has no attribute 'Y'``
  Occurs when an event ends-today.
  Fixed by changing the == operator of an event
  
Duplication of events:
* ``TypeError: open_duplicate_event_dialog_for_event() takes exactly 4 arguments (3 given)``
  Added missing argument

* ``AttributeError: 'NoneType' object has no attribute 'Y'``
  Check if event is visible before trying to find overlapping events.

* ``PyAssertionError: C++ assertion "strcmp(setlocale(LC_ALL, NULL), "C") == 0"... ``
  Occurs when date format is changed and then when Event editor is opened.
  A bmp works better than a png image when locale is used outside of wx.

Version 1.18.0
--------------

**Released on 30 July 2018.**

GUI:

* ``Added new representation of fuzzy edges when selecting view: Other Gradient Event box drawer with fuzzy edges.``
  (`#174 <https://sourceforge.net/p/thetimelineproj/backlog/174/>`_)
  
Fixed crash reports and bugs:

* ``Wrong editor is opened when right-click and selecting edit, on a milestone.``
  Check if event is milestone before selecting editor.

* ``Milestones can convert to ordinary events when a timeline is compressed.``
  Milestones is no longer part of the compression algorithm..

* ``Balloons are always shown for hooverd events.``
  Balloons are not shown if menu "View/Balloons on hover" is disabled.

* ``AttributeError: 'NoneType' object has no attribute 'get_ends_today'.``
  Event object existance is checked before getting attribute.

* ``InvalidOperationError: Circular category parent.``
  A circular parent is no longer possible to select. (This bug was introduced
  in the 1.16.0 release.)

Version 1.17.0
--------------

**Released on 25 Mars 2018.**

GUI:

* If the xml contains a description field for a container, it will now be
  displayed in a balloon, when hooverd.

* Selected events are not deselected when scrolling timeline with mouse.

* Events can be selected with alt + mouse drag.

* Events exported to listbox can now be filtered by visible categories

Fixed crash reports and bugs:

* ``PyAssertionError: C++ assertion "(itemid >= 0 && itemid < SHRT_MAX)``
  Eliminated menu id creation by using constant values.

* ``ValueError: Start time can't be after end time``
  This happened when ends-today flag was set, and start-time was in future.

* A change by another user is now detected when Timeline is closing.

* ``PyAssertionError: C++ assertion "node" failed at ..\..\src\msw\menu.cpp(863) in wxMenu::DoRemove(): bug in wxMenu::Remove logic``
  This happened when context menu has been used and another timeline is opened.

* It's now possible to change the background colour again.

Version 1.16.0
--------------

**Released on 13 November 2017.**

GUI:

* Using context menu no longer causes toolbar menu to stop working.

* Balloon text font is now settable in prefernces dialog.

* Sample text for font prefrences are now coloured also.

Fixed crash reports and bugs:

* ``AttributeError: 'NoneType' object has no attribute 'GetParent'``
  This happens when System info dialog is opened by context popup menu.



Version 1.15.0
--------------

**Released on 31 July 2017.**

GUI:

* Path to the configuration file is displayed in the System Info dialog.

* Date format is now displayed in the System Info dialog, as configured.

* Era rectangle is always visible, even when zooming out far.

* Text in a balloon can now be displayed besides or under an icon.

Fixed crash reports and bugs:

* ``UnicodeEncodeError: 'ascii' codec can't encode character u'\u03c0' in
  position 0: ordinal not in range(128)``
  This happened when the BC label contained non-ascii characters.

* ``UnicodeEncodeError: 'ascii' codec can't encode characters in position
  18-21: ordinal not in range(128)``
  This happened when a font face name contained non-ascii characters.

* Events highlighted during search sometimes get stuck in highlighted state.

* ``PyAssertionError: C++ assertion "!wxMouseCapture::stack.empty()" failed at 
  ..\..\src\common\wincmn.cpp(3319) in wxWindowBase::ReleaseMouse(): 
  Releasing mouse capture but capture stack empty?``
  This happens in when dragging the mouse from the calendar control.

Version 1.14.0
--------------

**Released on 8 May 2017.**

Calendar:

* BC years are formatted correctly in status bar.

* Decades and centuries are correctly represented around year 0 and in BC
  years. (Centuries are now denoted 1900s and represent the years 1900-1999.)

GUI:

* The formatting of the time duration for Gragorian time is more intuitive.

* All events can be selected with a menu command

* View selection to hide/show events done (progress = 100%).

* The limitation of number sizes has been removed in the numeric event editor.

* Now the position of the legend can be changed.

Fixed crash reports and bugs:

* Now weekends can be colorized again.
  (`#170 <https://sourceforge.net/p/thetimelineproj/backlog/170/>`_)

* It's no longer possible to close the milestone editor dialog with an invalid
  date/time.
  (`#171 <https://sourceforge.net/p/thetimelineproj/backlog/171/>`_)

* The event progress bar is now correctly drawn when event is partly outside of
  screen.

* ``OverflowError: long int too large to convert to float.``
  (`#126 <https://sourceforge.net/p/thetimelineproj/backlog/126/>`_)

* ``wx._core.PyAssertionError: C++ assertion "Assert failure" failed at
  ../src/gtk/menu.cpp(1300) in GetGtkHotKey(): unknown keyboard accel.``
  This was caused by incorrect translations.

* ``TypeError: %d format: a number is required, not TimeDelta.``
  This happened when trying to measure the distance between two overlapping
  events in a numeric timeline.

* ``IndexError: list index out of range.``
  This happened under some circumstances when zooming out far and scrolling to
  the far left.

* ``AttributeError: 'int' object has no attribute 'seconds'.``
  This happened when starting a slideshow with a numeric timeline.

Version 1.13.0
--------------

**Released on 31 January 2017.**

GUI:

* The naming strategy of overlapping Era's has been changed

* Major strip labels are drawn vertical when they don't fit in horizontal space.

* Balloon width is no longer dependent on the event width, so the text don't
  disappear to early.

Exporting:

* How to handle encoding errors, when exporting events to file, can now be selected.

* The events in a timeline can now be presented as a slideshow in a web browser.

Fixed crash reports and bugs:

* A Milestone can now have an empty text without crashing.
  (`#165 <https://sourceforge.net/p/thetimelineproj/backlog/165/>`_)

* Now an Era in a numeric timeline can have "ends today" without crashing.
  (`#166 <https://sourceforge.net/p/thetimelineproj/backlog/166/>`_)

* NotImplementedError: I don't believe this is in use.
  (`#168 <https://sourceforge.net/p/thetimelineproj/backlog/168/>`_)

* Now you can tab out of an invalid date field without crashing.
  (`#169 <https://sourceforge.net/p/thetimelineproj/backlog/169/>`_)

Version 1.12.0
--------------

**Released on 31 October 2016.**

GUI:

* Era's now have an ends-today property.
  (`#159 <https://sourceforge.net/p/thetimelineproj/backlog/159/>`_)

Documentation:

* Help pages updated.

Data:

* Option to switch off time for entire project.
  (`#157 <https://sourceforge.net/p/thetimelineproj/backlog/157/>`_)

* Sample text is displayed for fonts in the preference dialog

Export SVG:

* Eras are now drawn in the SVG image.
  (`#144 <https://sourceforge.net/p/thetimelineproj/backlog/144/>`_)

* Improved drawing of labels in SVG image.
  (`#145 <https://sourceforge.net/p/thetimelineproj/backlog/145/>`_)

* Timeline background colour is used used in SVG image.

Fixed crash reports and bugs:

* Milestones are handled correctly when undoing  changes.

* Duplicate categories in ics file is now handled correctly
  (`#160 <https://sourceforge.net/p/thetimelineproj/backlog/160/>`_)

* Invalid date and time entries, now generates error message.
  (`#163 <https://sourceforge.net/p/thetimelineproj/backlog/163/>`_)

* Creating exception message should not fail now.
  (`#161 <https://sourceforge.net/p/thetimelineproj/backlog/161/>`_)

* Duplicate dir names in directory Timeline is now handled.
  (`#162 <https://sourceforge.net/p/thetimelineproj/backlog/162/>`_)

Version 1.11.0
--------------

**Released on 2 August 2016.**

Data import:

* VTODO elements are now imported, as events, from ics files.
  (`#142 <https://sourceforge.net/p/thetimelineproj/backlog/142/>`_)

* Import options can now be specified when importing events, from ics files.
  (`#141 <https://sourceforge.net/p/thetimelineproj/backlog/141/>`_)

Data export:

* When exporting a timeline to images a merged image is also created.

Translations:

* Made label texts in 'Export to Listbox', translatable.
  (`#147 <https://sourceforge.net/p/thetimelineproj/backlog/147/>`_)

GUI:

* A checkmark can now be displayed in front of the event text when the event is done (100% progress).
  (`#134 <https://sourceforge.net/p/thetimelineproj/backlog/134/>`_)

* The duplicate event dialog can be opened from the event editor dialog
  (`#131 <https://sourceforge.net/p/thetimelineproj/backlog/131/>`_)

* After a search match the found event is highlighted

* The background colour can now be user defined.
  (`#151 <https://sourceforge.net/p/thetimelineproj/backlog/151/>`_)

Data:

* Introduced the special event type, Milestone.

Navigation:

* Now it's possible to return to the previous time period after a navigation.
  (`#153 <https://sourceforge.net/p/thetimelineproj/backlog/153/>`_)

Bug fixes:

* Bosparanian date format crashes.

* Timeline menu items are now disabled when no timeline is opened.
  (`#148 <https://sourceforge.net/p/thetimelineproj/backlog/148/>`_)

* Float division by zero when mouse moved.
  (`#150 <https://sourceforge.net/p/thetimelineproj/backlog/150/>`_)

Version 1.10.0
--------------

**Released on 30 April 2016.**

Calendar:

* Locale date formatter can now handle abbreviated month names in locale format
  pattern.
  (`#133 <https://sourceforge.net/p/thetimelineproj/backlog/133/>`_)

* The locale date format is now replaced with a user defined format

GUI:

* Users can now design and use their own icons for fuzzy, locked, and hyperlink.
  (`#93 <https://sourceforge.net/p/thetimelineproj/backlog/93/>`_)

* The vertical zoom (menu or Alt +/-) now zooms instead of scrolling.

* Ctrl+Shift+MouseWheel now scrolls vertically instead of zooming.

* Marking invalid dates with pink background now works correctly even in
  Windows.

* The date controls should now follow the locale date formatting setting.

* Weekdays can now have a colour different from the background.

* Scrolling timeline after regaining focus now works properly even in
  Windows.
  (`#138 <https://sourceforge.net/p/thetimelineproj/backlog/138/>`_)

* The vertical space between events is now a user settable preference.

Translations:

* The BC string in strips is now translatable

Fixed crash reports:

* The Timeline xml file is updated when an Era is deleted
  (`#139 <https://sourceforge.net/p/thetimelineproj/backlog/139/>`_)

* Import events dialog gives UnicodeEncodeError if exceptions contain unicode
  messages.

Import:

* Categories are now created when importing ics data
  (`#141 <https://sourceforge.net/p/thetimelineproj/backlog/141/>`_)

Export:

* Data in Export to Listbox can now be copied to clip board
  (`#146 <https://sourceforge.net/p/thetimelineproj/backlog/146/>`_)

Version 1.9.0
-------------

**Released on 31 January 2016.**

Calendar:

* Locale date formats correctly at start of timeline.
  (`#116 <https://sourceforge.net/p/thetimelineproj/backlog/116/>`_)

GUI:

* There is an optional tool bar that contains buttons for toggling some
  settings.

* "To time" in event editor is correctly laid out when checking "Period".

* Images can be dragged and dropped on an event to change icon.
  (`#103 <https://sourceforge.net/p/thetimelineproj/backlog/103/>`_)

* A preference decides if the time checkbox is checked for new events.
  (`#119 <https://sourceforge.net/p/thetimelineproj/backlog/119/>`_)

* Subevents in a container can be locked if the extended container strategy is
  used.
  (`#110 <https://sourceforge.net/p/thetimelineproj/backlog/110/>`_)

* The description text in the event editor can be selected with Ctrl+A.
  (`#115 <https://sourceforge.net/p/thetimelineproj/backlog/115/>`_)

* The ends-today checkbox in the event editor is enabled when the editor is
  opened from the menu.
  (`#114 <https://sourceforge.net/p/thetimelineproj/backlog/114/>`_)

* The events in the exported list are sorted by start date.
  (`#106 <https://sourceforge.net/p/thetimelineproj/backlog/106/>`_)

* Colors can be selected for major strip lines, minor strip lines and now line.
  (`#111 <https://sourceforge.net/p/thetimelineproj/backlog/111/>`_)

* Overlapping eras are now displayed in a mixed color.
  (`#108 <https://sourceforge.net/p/thetimelineproj/backlog/108/>`_)

* Colors can now be selected for events without an associated category.
  (`#81 <https://sourceforge.net/p/thetimelineproj/backlog/81/>`_)

* The Ends-today property can be set on subevents if the extended container
  strategy is used.

* A new dialog in the help menu displays System information.

Translations:

* The wx stock items are translated correctly in the Windows binary.
  (`#109 <https://sourceforge.net/p/thetimelineproj/backlog/109/>`_)

* The strip text 'Century' is translatable.
  (`#107 <https://sourceforge.net/p/thetimelineproj/backlog/107/>`_)

Bug fixes:

* Edit event dialog does not crash when there is a db error.
  (`#127 <https://sourceforge.net/p/thetimelineproj/backlog/127/>`_)

* Application does not crash at startup if system has locale zh_CN (Chinese).
  (Merged from 1.5.1.)

* Application does not crash when duplicating container events.
  (`#125 <https://sourceforge.net/p/thetimelineproj/backlog/125/>`_)

Version 1.8.1
-------------

**Released on 10 November 2015.**

This is a bugfix release. It fixes a critical bug that disables editing numerical timelines.

Fixed crash reports:

* ``AttributeError: 'NumTimePicker' object has no attribute 'show_time'``
  (`#117 <https://sourceforge.net/p/thetimelineproj/backlog/117/>`_)

Version 1.8.0
-------------

**Released on 31 October 2015.**

This is a periodic release.

Calendar:

* Timelines can be created using the "The Dark Eye" (Das Schwarze Auge, DSA)
  official calender.

Drawing:

* When you scroll vertically by dragging, the view moves proportionally.
  (`#88 <https://sourceforge.net/p/thetimelineproj/backlog/88/>`_)

* Containers expand vertically when they contain overlapping events.
  This is an experimental feature that must be enabled.
  (`#39 <https://sourceforge.net/p/thetimelineproj/backlog/39/>`_)

* You can zoom out to a period longer than 1200 years. There is no longer a
  limit.
  (`#90 <https://sourceforge.net/p/thetimelineproj/backlog/90/>`_)

Exporting:

* Exporting to CSV behaves properly when there is a newline in the description
  of an event.
  (`#92 <https://sourceforge.net/p/thetimelineproj/backlog/92/>`_)

GUI:

* All dialogs have a polished and more uniform look.

* When creating a new timeline, a dialog pops up that let's you choose what
  type of timeline you want to create.
  (`#97 <https://sourceforge.net/p/thetimelineproj/backlog/97/>`_)

* Event and eras can be created with a period longer than 1200 years. There is
  no longer a limit.
  (`#98 <https://sourceforge.net/p/thetimelineproj/backlog/98/>`_)

* When duplicating an event with period month it behaves properly in edge
  cases.

Fixed crash reports:

* ``PyAssertionError: C++ assertion "wxAssertFailure" failed at ..\..\src\common\stockitem.cpp(166) in wxGetStockLabel(): invalid stock item ID``
  (`#95 <https://sourceforge.net/p/thetimelineproj/backlog/95/>`_)

* ``KeyError: <bound method Font.Underlined of <timelinelib.wxgui.components.font.Font; proxy of <Swig Object of type 'wxFont *' at 0x8f240f0> >>``
  (`#83 <https://sourceforge.net/p/thetimelineproj/backlog/83/>`_)

* ``string index out of range``
  (`#85 <https://sourceforge.net/p/thetimelineproj/backlog/85/>`_)

* ``AttributeError: 'NoneType' object has no attribute 'julian_day'``
  (`#96 <https://sourceforge.net/p/thetimelineproj/backlog/96/>`_)

* ``ValueError: julian_day must be >= 0``
  (`#79 <https://sourceforge.net/p/thetimelineproj/backlog/79/>`_)

* ``LockedException: Unable to take lock on ...``
  (`#105 <https://sourceforge.net/p/thetimelineproj/backlog/105/>`_)

Version 1.7.1
-------------

**Released on 17 August 2015.**

This is a bugfix release. It fixes a critical bug where data could be lost.

Data:

* Content of .timeline file is not erased when it is opened. This was a bug
  that has now been fixed.

Drawing:

* Minor strip font is only bold for weekend days. A bug made it a bit random
  before.

Fixed crash reports:

* ``AttributeError: 'module' object has no attribute 'Color'``

* ``AttributeError: 'EventEditorDialog' object has no attribute 'set_focus'``
  (`#89 <https://sourceforge.net/p/thetimelineproj/backlog/89/>`_)

Version 1.7.0
-------------

**Released on 30 July 2015.**

This is a periodic release of Timeline. It contains many solutions to problems
identified by users of Timeline.

Data:

* Events can have multiple hyperlinks.
  (`#30 <https://sourceforge.net/p/thetimelineproj/backlog/30/>`_)

* An experimental feature allows entering dates before 4714 BC. This allows
  larger time periods to be created.
  (`#51 <https://sourceforge.net/p/thetimelineproj/backlog/51/>`_)

Drawing:

* An icon is drawn in the event box if it has hyperlinks. This makes it easier
  to see which events have hyperlinks.
  (`#29 <https://sourceforge.net/p/thetimelineproj/backlog/29/>`_)

* Period events can be configured to never be drawn above the center line. This
  should make it more obvious which events are period events and which are
  point events.
  (`#42 <https://sourceforge.net/p/thetimelineproj/backlog/42/>`_, `#46 <https://sourceforge.net/p/thetimelineproj/backlog/46/>`_)

* A setting exist that decides if event texts should be centered or not.
  (`#73 <https://sourceforge.net/p/thetimelineproj/backlog/73>`_)

* There is no horizontal padding between events. This allows more events to fit
  on the screen.
  (`#2 <https://sourceforge.net/p/thetimelineproj/backlog/2>`_)

* Some fonts used to draw the timeline can be customized. This should allow
  users to customize the look of their timelines to their taste.
  (`#63 <https://sourceforge.net/p/thetimelineproj/backlog/63>`_)

* A setting can draw point events with the left box edge at the vertical line.
  This makes it more clear where the event starts in time.
  (`#60 <https://sourceforge.net/p/thetimelineproj/backlog/60/>`_)

GUI:

* A notification is shown when a shortcut is saved.
  (`#23 <https://sourceforge.net/p/thetimelineproj/backlog/23/>`_)

* The category editor can be opened with double click. This makes the intuitive
  way to open the editor possible.
  (`#47 <https://sourceforge.net/p/thetimelineproj/backlog/47/>`_)

* The period checkbox in the event editor remembers its value from last time.
  This should speed up entering of period events.
  (`#28 <https://sourceforge.net/p/thetimelineproj/backlog/28>`_)

* Multiple events can be added to a category by selecting them and selecting a
  context menu item. This should make it more convenient to assign categories.
  (`#67 <https://sourceforge.net/p/thetimelineproj/backlog/67>`_)

* The tab-order of controls in the event editor dialog can be customized. This
  allows users to put their most frequently used controls first.
  (`#62 <https://sourceforge.net/p/thetimelineproj/backlog/62>`_)

* The divider line can be adjusted with mouse dragging. This should make it
  more convenient to use Timeline on a touch device.
  (`#58 <https://sourceforge.net/p/thetimelineproj/backlog/58>`_)

* Events can be moved vertically by selecting them and pressing Up/Down or
  selecting menu items. This makes it more obvious how to move events
  vertically.
  (`#45 <https://sourceforge.net/p/thetimelineproj/backlog/45/>`_)

Exporting:

* Exporting a whole timeline to several images now preserves the vertical position
  of events between images. So now images can be put together and the events
  will align correctly.
  (`#72 <https://sourceforge.net/p/thetimelineproj/backlog/72/>`_)

Misc:

* Undo works after compress. This allows users to undo compress action if
  the result was not desirable.
  (`#65 <https://sourceforge.net/p/thetimelineproj/backlog/65/>`_)

* Does not fail to open Timeline files that have period wider than 1200 years.
  This should prevent users from having to manually edit the xml file.
  (`#8 <https://sourceforge.net/p/thetimelineproj/backlog/8/>`_)

* Crash reports have information about locale settings. This makes it easier to
  troubleshoot errors depending on locale settings.
  (`#54 <https://sourceforge.net/p/thetimelineproj/backlog/54/>`_)

Fixed crash reports:

* ``AttributeError: 'EraEditorDialog' object has no attribute 'on_return'``
  (`#57 <https://sourceforge.net/p/thetimelineproj/backlog/57/>`_)

* ``KeyError: '33'``
  (`#53 <https://sourceforge.net/p/thetimelineproj/backlog/53/>`_)

* ``KeyError: 'Nov'``
  (`#50 <https://sourceforge.net/p/thetimelineproj/backlog/50/>`_)

* ``ValueError: Invalid date.``
  (`#55 <https://sourceforge.net/p/thetimelineproj/backlog/55/>`_)

* ``LockedException: Unable to take lock on...``
  (`#69 <https://sourceforge.net/p/thetimelineproj/backlog/69>`_)

* ``OverflowError: long int too large to convert to float``
  (`#75 <https://sourceforge.net/p/thetimelineproj/backlog/75>`_)

* ``Exception: No timeline set``
  (`#56 <https://sourceforge.net/p/thetimelineproj/backlog/56>`_)

* ``TypeError: unsupported operand type(s) for +: 'int' and 'TimeDelta'``
  (`#48 <https://sourceforge.net/p/thetimelineproj/backlog/48/>`_, `#78 <https://sourceforge.net/p/thetimelineproj/backlog/78>`_)

* ``WindowsError: [Error 32] The process cannot access the file because it is
  being used by another process``
  (`#33 <https://sourceforge.net/p/thetimelineproj/backlog/33/>`_)

* ``UnicodeEncodeError: 'ascii' codec can't encode character u'\xc9' in
  position 0: ordinal not in range(128)``
  (`#49 <https://sourceforge.net/p/thetimelineproj/backlog/49>`_)

Windows specific:

* The log file is created in a standard user temp directory. This ensures that
  even if Timeline is installed in a read-only location, the log file can be
  created.
  (`#74 <https://sourceforge.net/p/thetimelineproj/backlog/74>`_)

* Broken fragments of sidebar is not shown at startup.
  (`#52 <https://sourceforge.net/p/thetimelineproj/backlog/52/>`_)

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

Version 1.5.1
-------------

**Released on 4 December 2015.**

Bug fixes:

* Application does not crash at startup if system has locale zh_CN (Chinese)

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
