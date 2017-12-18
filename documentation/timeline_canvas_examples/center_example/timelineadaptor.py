def make_sure_timelinelib_can_be_imported():
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "source"))


def install_gettext_in_builtin_namespace():
    def _(message):
        return message
    import __builtin__
    if not "_" in __builtin__.__dict__:
        __builtin__.__dict__["_"] = _


make_sure_timelinelib_can_be_imported()
install_gettext_in_builtin_namespace()
