Build a Dialog window
=====================

This pattern is inspired by the `Humbe Dialog Box
<http://www.objectmentor.com/resources/articles/TheHumbleDialogBox.pdf>`_.

The control object
------------------
To make it easier to test a Dialog we follow  a pattern where all business logic is placed in a class of its own, which we call the controller class.
The controller is instantiated in the __init__ function of the Dialog class like this::

    def __init__(self, timeline, ...):
        self.controller = MyDialogControllet (self, timeline)

Notice that the constructor takes a reference to the Dialog as first argument.
The controller __init__ function looks like this::

    def __init__(self, view):
        self.view = view

The Dialog class should contain no business logic at all. It should only contain simple logic to administer the gui objects within the Dialog. 
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
   * Initiation of gui sperclass
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
We try to break the cretion of the gui into small functions.
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
 
