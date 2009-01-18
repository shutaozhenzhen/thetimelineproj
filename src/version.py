VERSION = (0, 1, 0)
DEV = True


def get_version():
    if DEV:
        return "%s.%s.%sdev" % VERSION
    return "%s.%s.%s" % VERSION
