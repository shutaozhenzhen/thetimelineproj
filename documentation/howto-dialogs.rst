Build a dialog widget
=====================

This howto describes how we like to build dialog widgets (``wx.Dialog``).

To get started, we have a tool that can generate boilerplate code. Let's try
it::

    python3 tools/dialog_template.py

If we enter the name ``TestDialog``, the following files will be created for
us::

    source/timelinelib/wxgui/dialogs/testdialog/__init__.py
    source/timelinelib/wxgui/dialogs/testdialog/testdialog.py
    source/timelinelib/wxgui/dialogs/testdialog/testdialogcontroller.py
    test/specs/wxgui/dialogs/testdialog/__init__.py
    test/specs/wxgui/dialogs/testdialog/testdialog.py

Essentially, a dialog consists of 3 files: the dialog itself, the controller,
and the test file.

The dialog and the controller collaborate in a pattern inspired by the
`Humbe Dialog Box <http://www.objectmentor.com/resources/articles/TheHumbleDialogBox.pdf>`_.
The dialog corresponds to the view and the controller corresponds to the smart
object.

What the boiler plate code has given us is a way to test our dialog. Let's try
the following command::

    python3 tools/execute-specs.py --halt-gui --only testdialog

A dialog shows up with a hello world button.

The ``--halt-gui`` flag ensures that the dialog stays open until we manually
close it. That is not desirable when running tests automatically because it
needs manual inspection, but for quickly inspecting our dialog, it's perfect.

Let's try without the ``--halt-gui`` flag just to ensure that it works::

    python3 tools/execute-specs.py --only testdialog

Now let's look at how the GUI elements are created. Here is
``source/timelinelib/wxgui/dialogs/testdialog/testdialog.py`` without the
copyright notice::

    from timelinelib.wxgui.dialogs.testdialog.testdialogcontroller import TestDialogController
    from timelinelib.wxgui.framework import Dialog


    class TestDialog(Dialog):

        """
        <BoxSizerVertical>
            <Button label="$(test_text)" />
        </BoxSizerVertical>
        """

        def __init__(self, parent):
            Dialog.__init__(self, TestDialogController, parent, {
                "test_text": "Hello World",
            }, title=_("New dialog title"))
            self.controller.on_init()

Notice the docstring that contains XML. That XML describes the GUI elements
that are present in the dialog and how they are laid out.

Let's try to change the XML to the following::

        <BoxSizerVertical>
            <Button label="$(test_text)" />
            <BoxSizerHorizontal>
                <TextCtrl id="text_one" />
                <TextCtrl id="text_two" />
            </BoxSizerHorizontal>
        </BoxSizerVertical>

And run the test again::

    python3 tools/execute-specs.py --halt-gui --only testdialog

We see that the elements are laid out as described in the XML.

Now let's implement some functionality. When we press the button we want to
fill the text widgets with some text. The way this is going to work is that the
dialog will send an event to the controller, the controller then calls methods
on the dialog to update some part.

First, let's connect the event by changing the XML for the button::

    <Button label="$(test_text)" event_EVT_BUTTON="on_click" />

We also need to add the appropriate method in the controller. The controller
(``source/timelinelib/wxgui/dialogs/testdialog/testdialogcontroller.py``)
should now look like this::

    from timelinelib.wxgui.framework import Controller


    class TestDialogController(Controller):

        def on_init(self):
            pass

        def on_click(self, event):
            pass

If we run the test again, it will not crash, but nothing happens when we click
the button. Let's change the ``on_click`` method to call methods on the dialog
(referred to as the view)::

    def on_click(self, event):
        self.view.SetTextOne("hello")
        self.view.SetTextTwo("world")

And let's add the two methods in the dialog class::

    def SetTextOne(self, text):
        self.text_one.SetValue(text)

    def SetTextTwo(self, text):
        self.text_two.SetValue(text)

``self.text_one`` and ``self.text_two`` were automatically created because we
assigned those ids to the controls in the xml.

If we run the tests again and press the button, the texts should be updated.

One purpose for splitting a dialog into a GUI part and a controller part is to
make the controller testable in isolation. The idea is to put most of the
dialog logic in the controller and test that independently of the GUI.

Let's try to add a test of this kind to
``test/specs/wxgui/dialogs/testdialog/testdialog.py``::

    def test_it_populates_text_when_button_is_clicked(self):
        self.controller.on_click(wx.CommandEvent())
        self.view.SetTextOne.assert_called_with("Hello")

Let's run the tests again (but this time there is no need to halt the gui)::

    python3 tools/execute-specs.py --only testdialog

We see this::

    AssertionError: Expected: (('Hello',), {})
    Called with: (('hello',), {})

There is a missmatch between the value we set and the value we expect to be set
in the first text field. We have to figure out which one is correct, fix it,
and move on.

The control object
------------------
To make it easier to test a Dialog we follow  a pattern where all business logic is placed in a class of its own, which we call the controller class.
The controller is instantiated in the __init__ function of the Dialog class like this::

    def __init__(self, timeline, ...):
        self.controller = MyDialogController (self, timeline)

Notice that the constructor takes a reference to the Dialog as first argument.
The controller __init__ function looks like this::

    def __init__(self, view):
        self.view = view

The Dialog class should contain no business logic at all. It should only contain simple logic to handle the gui objects within the Dialog. 
For example to set a value in a TextBox the Dialog, the dialog shall provide a method set_text(text)  that can be used by the controller. 
For the same reason it must provide a get_text() function that the controller can use to retrieve values entered by a user.

When it comes to testing the Dialog class is mocked out which means that the test dont have to deal with gui objects. 
It can be verified that Dialog functions are called when code in the controller is tested.
We assume for example that the Dialog.set_text() function puts the text in the TextBox control. 
We can verify this by running the app. If it works once, we assume it will work the next time also.
That means we can concentrate on testing the business logic in the controller.
::

    +------------+                   +-------------------+
    |            |controller     view|                   |
    | GUI object |<=================>| Controller object |
    |            |                   |                   |
    +------------+                   +-------------------+


The gui constructor
-------------------
The gui constructor typically contains the following
   * Initiation of gui superclass
   * Call to the create_gui() method
   * Creation of controller object
   * Tell the controller to populate the dialog

Sample::

    class MyDialog(wx.Dialog):

        def __init__(self, parent, data):
            wx.Dialog.__init__(self, parent, title="mydialog", name="my_dialog", 
                               style=wx.DEFAULT_DIALOG_STYLE)
            self._create_gui()
            self.controller = MyController(self)
            self.controller.populate()


    class MyController(object)

        def __init__(self, view, data)
            self.view = view
            self.data = data

        def populate(self):
            self.view.set_name(self.data.name)
        
        
Sizers and controls
-------------------
We try to break the creation of the gui into small functions.
Normally a sizer is passed to a function. The idea is that the function shall create som objects
and place them in the sizer::

    def _create_checkbox_add_more(self, sizer):
        label = _("Add more events after this one")
        self.chb_add_more = wx.CheckBox(self, label=label)
        sizer.Add(self.chb_add_more, flag=wx.ALL, border=BORDER)

Controls that need to be referenced later are added to the dialog object (self).


Helper methods
--------------
Some problem tends to repeat themselves. So to avoid duplicate code it's desirable to have that peace of code defined once.
The place to define such code is in the wxgui.utils package.
In this package the following gui helper code can be found:

 * WildcardHelper       A class used to define file types in a open/save file dialog
 * get_color            Takes an rgb tuple as argument and returns a wx:Colour object
 * set_wait_cursor      Changes the cursor for the given gui window to a wait cursor
 * set_default_cursor   Changes the cursor for the given gui window to a default cursor   
 * get_user_ack         Displayes a message box with a given message and returns true if the user pressed the YES button.
                        The follwing three displays e message box with a given message.
 * display_information_message
 * display_warning_message
 * display_error_message
 * show_modal           Show a modal dialog using error handling pattern
 
Module structure
----------------
The dialog class and the controller class are typically saved in separate source files and
these files are placed in a module under source.timelinelib.wxgui.dialogs.

The tests for these classes are placed in a module under test.specs.wxgui.dialogs.

Calling updating dialogs
------------------------
When a dialog is used to change data in a timeline, it's important that the mechanism to
prevent two users to change a timeline at the same time, somes into play.

For that reason an updating dialog should always be opened through the helper function
self_locking. Like the code where the EventEditorDialog is opened:

Sample::

    def open_event_editor_for(parent, config, db, handle_db_error, event):
        def create_event_editor():
            if event.is_container():
                title = _("Edit Container")
                return ContainerEditorDialog(parent, title, db, event)
            else:
                return EventEditorDialog(
                    parent, config, _("Edit Event"), db, event=event)
        def edit_function():
            gui_utils.show_modal(create_event_editor, handle_db_error)
        safe_locking(parent, edit_function)
