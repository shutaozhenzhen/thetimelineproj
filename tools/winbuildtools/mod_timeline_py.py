import sys
import os


FILE = "timeline.py"


def main():
    project_dir = sys.argv[1]
    target = os.path.join(project_dir, "source", "timeline.py")
    print "Script: mod2_timeline_py.py"
    print "Target:", target
    
    f = open(target, "r")
    text = f.read()
    f.close()
    f = open(target, "w")
    lines = text.split("\n")
    for line in lines:
        if line[0:16] == "sys.path.insert(":
            f.write("exepath = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))\n")
            f.write("sys.path.insert(0, exepath)\n")
        else:
            f.write(line + "\n")
    f.close()


if __name__ == "__main__":
    main()
