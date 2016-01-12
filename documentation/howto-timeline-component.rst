How to use Timeline component in your wxPython application
==========================================================

**Note: This is a work in progress.**

The core component in Timeline, the canvas where events are drawn, is a
reusable component that any wxPython application can use. It might be extracted
to its own project. This page documents how to use the component.

Importing
---------

All code related to the timeline canvas is located in ``timelinelib.canvas``.
We must obtain the source code and make sure that the ``source/timelinelib``
folder is on our Python path.

For the time being, we also need to install gettext. The canvas currently
depends on gettext, but it should not in the future. We can use this function
to install gettext:

.. literalinclude:: timeline_canvas_examples.py
    :language: python
    :pyobject: install_gettext_in_builtin_namespace

Now we should be able to import the ``TimelineCanvas`` like this:

.. literalinclude:: timeline_canvas_examples.py
    :language: python
    :lines: 36

The canvas
----------

The ``TimelineCanvas`` is a wx control that takes a single argument: the parent
control:

.. py:class:: timelinelib.canvas.TimelineCanvas

    .. py:method:: __init__(parent)

It can be used in a frame like this:

.. literalinclude:: timeline_canvas_examples.py
    :language: python
    :pyobject: EmptyCanvas

Navigation
----------

The following functions change the time period that is displayed in the canvas.

.. py:method:: timelinelib.canvas.TimelineCanvas.Navigate(navigation_fn)

    This is the most generic navigation function. It is used by all the other
    navigation functions. It takes a function that is called with one argument,
    the time period, and should return a new time period. The return value is
    the new time period that is displayed.

.. py:method:: timelinelib.canvas.TimelineCanvas.Scroll(factor)

Exporting
---------

.. py:method:: timelinelib.canvas.TimelineCanvas.SaveAsPng(path)

.. py:method:: timelinelib.canvas.TimelineCanvas.SaveAsSvg(path)
