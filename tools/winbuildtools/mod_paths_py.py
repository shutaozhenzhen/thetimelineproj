import sys
import os


def main():
    project_dir = sys.argv[1]
    target = os.path.join(project_dir, "source", "timelinelib", "config", "paths.py")
    print "Script: mod2_paths_py.py"
    print "Target:", target

    f = open(target, "r")
    text = f.read()
    f.close()
    f = open(target, "w")
    lines = text.split("\n")
    for line in lines:
        if line[0:7] == "_ROOT =":
            f.write("import sys\n")
            f.write("_ROOT = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))\n")
        else:
            f.write(line + "\n")
    f.close()


if __name__ == "__main__":
    main()
