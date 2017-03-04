Architecture overview
=====================

This page intends to explain the internal architecture of Timeline on a high
level.

This page includes diagrams of some of the classes in Timeline. They can remind
you of how classes work, but they are not intended to fully explain the code.

GUI classes
-----------

.. image:: /images/classes-gui-overview.png

Drawing
-------

.. image:: /images/classes-drawing.png

For the purpose of making testing easier we try to divide gui-components in two
parts: the GUI class itself and another class, the controller, containing the
'business' logic. The goal is to have no 'business' logic at all in the GUI
class. It should only have simple gui actions.

Another design decision for the purpose of making testing easier is to inject
objects into the constructor of a class. This can be seen here when the
``DrawingArePanel`` creates its controller, the ``DrawingArea``, it passes the
drawer object in the constructor, ``get_drawer()``.

Startup
-------

.. image:: /images/classes-startup.png


System documentation - API
--------------------------
`System documentation <http://www.rolidata.se/rldweb3/timeline_sysdoc/>`_.
