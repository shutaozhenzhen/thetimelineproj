CODE = """\
        import zipfile
        file = zipfile.ZipFile("library.zip", "r")
        names = []
        for name in file.namelist():
            if name.startswith("timelinelib/plugin/plugins/"):
                name = name[27:]
                #name = name.rsplit("/", 1)[1]
                if name.endswith(".pyc") and not "__" in name:
                    name = name.split(".")[0]
                    name = name.replace("/", ".")
                    names.append(name)
        f = open("test.txt", "w")
        f.write(" ".join(names))
        f.close()
        return [self._import_module("timelinelib.plugin.plugins.%s" % mod) for mod in names]        
"""


FILE = "timelinelib\\plugin\\factory.py"
f = open(FILE, "r")
text = f.read()
f.close()
f = open(FILE, "w")
lines = text.split("\n")
state = 0
for line in lines:
    if state == 1:
        if len(line.strip()) == 0:
            f.write(line + "\n")
            state = 0
    else:
        if "def _get_candidate_modules(self):" in line:
            f.write(line + "\n")
            f.write(CODE)
            state = 1
        else:
            f.write(line + "\n")
f.write("\n")        
f.write("import timelinelib.plugin.plugins.backgrounddrawers.defaultbgdrawer\n")
f.write("import timelinelib.plugin.plugins.eventboxdrawers.defaulteventboxdrawer\n")
f.write("import timelinelib.plugin.plugins.eventboxdrawers.gradienteventboxdrawer\n")
f.write("import timelinelib.plugin.plugins.eventboxdrawers.othergradienteventboxdrawer\n")
f.write("import timelinelib.plugin.plugins.exporters.exporttobitmap\n")
f.write("import timelinelib.plugin.plugins.exporters.exporttolist\n")
f.write("import timelinelib.plugin.plugins.exporters.exporttosvg\n")
f.write("import timelinelib.plugin.plugins.exporters.timelineexporter\n")

f.close()
