How to use Timeline component in your wxPython application
==========================================================

**Note: This is work in progress and feedback is welcome.**

The core component in Timeline, the canvas where events are drawn, is a
reusable component that any wxPython application can use. This page documents
how to use that component.

Importing
---------

Currently, the canvas component is embedded in the Timeline source code.  All
code related to the canvas component is located in ``timelinelib.canvas``. This
is not 100% true because the canvas component depends on other parts of
``timelinelib``. The long term goal though is that it shouldn't so that the
``timelinelib.canvas`` package can be extracted to its own project.

In order to use the canvas component, we must obtain the Timeline source code
and make sure that the ``source/timelinelib`` folder is on our Python path.

For the time being, we also need to setup the gettext translation function.
The canvas currently depends on gettext, but it should not in the future. We
can use this function to setup gettext:

.. literalinclude:: timeline_canvas_examples.py
    :language: python
    :pyobject: install_gettext_in_builtin_namespace

.. HINT::

    If we get an error similar to the one bellow, gettext has not been properly
    setup::

        Traceback (most recent call last):
          ..
        NameError: name '_' is not defined

Example
-------

Here is a complete example how to use the canvas component:

.. literalinclude:: timeline_canvas_examples.py
    :language: python
    :lines: 14-

The canvas
----------

The ``TimelineCanvas`` is a wx control that takes a single argument: the parent
control.

.. py:class:: timelinelib.canvas.TimelineCanvas

    .. py:method:: __init__(parent)

Navigation
^^^^^^^^^^

The following functions change the time period that is displayed in the canvas.

.. py:method:: timelinelib.canvas.TimelineCanvas.Navigate(navigation_fn)

    This is the most generic navigation function. It is used by all the other
    navigation functions. It takes a function that is called with one argument,
    the time period, and should return a new time period. The return value is
    the new time period that is displayed.

.. py:method:: timelinelib.canvas.TimelineCanvas.Scroll(factor)

Exporting
^^^^^^^^^

.. py:method:: timelinelib.canvas.TimelineCanvas.SaveAsPng(path)

.. py:method:: timelinelib.canvas.TimelineCanvas.SaveAsSvg(path)
