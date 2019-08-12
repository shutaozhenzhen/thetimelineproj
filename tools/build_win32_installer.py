# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018  Rickard Lindberg, Roger Lindberg
#
# This file is part of Timeline.
#
# Timeline is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Timeline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Timeline.  If not, see <http://www.gnu.org/licenses/>.


"""
Working directory = BUILD_DIR
COPYDIR     Copies from TIMELINE_DIR to BUILD_DIR
"""

import argparse
import sys
import os
import shutil
import tempfile
import subprocess
import timelinetools.packaging.repository


TIMELINE_DIR = os.path.abspath("..\\..\\")
BUILD_DIR = os.path.abspath(".\\target")
ARCHIVE = "archive"
ARTIFACT = "artifact"

COPYFILE = 0
COPYDIR = 1
PUSHD = 3
POPD = 4
RUNCMD = 5
RUNPYSCRIPT = 6
ANNOTATE = 8
RUNPYTEST = 9

ACTION_NAMES = {COPYFILE: "COPYFILE",
                COPYDIR: "COPYDIR",
                PUSHD: "PUSHD",
                POPD: "POPD",
                RUNCMD: "RUNCMD",
                RUNPYSCRIPT: "RUNPYSCRIPT",
                RUNPYTEST: "RUNPYTEST"
                }


known_targets = ("win32Installer")


win32InstallerActions = (
    (ANNOTATE, "Run Tests", ""),
    (RUNPYTEST, ["tools", "execute-specs.py"], ""),

    (ANNOTATE, "Modify source files", ""),
    (RUNPYSCRIPT, ["tools", "winbuildtools", "mod_timeline_py.py"], ""),
    (RUNPYSCRIPT, ["tools", "winbuildtools", "mod_paths_py.py"], ""),
    (RUNPYSCRIPT, ["tools", "winbuildtools", "mod_version_py.py"], ""),
    (RUNPYSCRIPT, ["tools", "winbuildtools", "mod_factory_py.py"], ""),
    (RUNPYSCRIPT, ["tools", "winbuildtools", "mod_timeline_iss_win32.py"], ""),

    (ANNOTATE, "Create a target directory for the build", ""),
    (COPYDIR, ["source", "timelinelib"], ["builddir", "timelinelib"]),
    (COPYDIR, ["dependencies", "timelinelib", "icalendar-3.2\icalendar"], ["builddir", "icalendar"]),
    (COPYDIR, ["dependencies", "timelinelib", "pytz-2012j\pytz"], ["builddir", "pytz"]),
    (COPYDIR, ["dependencies", "timelinelib", "pysvg-0.2.1\pysvg"], ["builddir", "pysvg"]),
    (COPYDIR, ["dependencies", "timelinelib", "markdown-2.0.3", "markdown"], ["builddir", "markdown"]),
    (COPYDIR, ["dependencies", "timelinelib", "Pillow-3.2.0", "PIL"], ["builddir", "pillow"]),
    (COPYDIR, ["tools", "winbuildtools", "inno"], ["builddir", "inno"]),
    (COPYFILE, ["source", "timeline.py"], ["builddir", "timeline.py"]),
    (COPYFILE, ["tools", "winbuildtools", "setup.py"], ["builddir", "setup.py"]),
    (COPYFILE, ["COPYING"], ["builddir", "COPYING"]),
    (COPYFILE, ["tools", "winbuildtools", "inno", "WINSTALL"], ["builddir", "WINSTALL"]),

    (ANNOTATE, "Create distribution directory", ""),
    (COPYDIR, ["icons"], ["builddir", "icons"]),
    (RUNPYSCRIPT, ["builddir", "setup.py"], "py2exe"),
    (COPYDIR, ["translations"], ["builddir", "dist", "translations"]),
    (COPYDIR, ["icons"], ["builddir", "dist", "icons"]),
    (COPYDIR, ["tools"], ["builddir", "dist", "tools"]),

    (ANNOTATE, "Create installer executable", ""),
    (RUNCMD, "python", ["builddir", "dist", "tools", "generate-mo-files.py"]),

    (ANNOTATE, "Create Setup executable", ""),
    (RUNCMD, "iscc.exe", ["builddir", "inno", "timelineWin32.iss"]),

    (ANNOTATE, "Deliver executable artifact", ""),
    (COPYFILE, [ARTIFACT], [ARTIFACT]),

    (ANNOTATE, "Done", ""),
)


actions = {"win32Installer": win32InstallerActions}


class Target():

    def __init__(self, target):
        print("-------------------------------------------------------")
        print("  %s" % ("Building target %s" % target))
        print("-------------------------------------------------------")
        self.target = target
        self.actions = actions[target]
        self.ACTION_METHODS = {COPYFILE: self.copyfile,
                               COPYDIR: self.copydir,
                               PUSHD: self.pushd,
                               POPD: self.popd,
                               RUNCMD: self.runcmd,
                               RUNPYSCRIPT: self.runpyscript,
                               RUNPYTEST: self.runpytest,
                               ANNOTATE: self.annotate}

    def build(self, arguments, artifact_dir):
        temp_dir = tempfile.mkdtemp()
        try:
            self.assert_that_target_is_known()
            self.setup_and_create_directories(arguments, artifact_dir, temp_dir)
            self.execute_actions()
        finally:
            shutil.rmtree(temp_dir)
            pass

    def assert_that_target_is_known(self):
        if self.target not in known_targets:
            print("The target %s is unknown" % self.target)
            print("BUILD FAILED")
            sys.exit(1)

    def setup_and_create_directories(self, arguments, artifact_dir, temp_dir):
        self.artifact_dir = artifact_dir
        self.project_dir = self.create_project_directory(arguments, temp_dir)
        print("Artifact dir: %s" % self.artifact_dir)
        print("Project dir:  %s" % self.project_dir)
        print("Working dir:  %s" % os.getcwd())

    def create_project_directory(self, arguments, temp_dir):
        print("Create project directory")
        repository = timelinetools.packaging.repository.Repository()
        self.archive = repository.archive(arguments.revision, temp_dir, ARCHIVE)
        return os.path.join(temp_dir, ARCHIVE)

    def execute_actions(self):
        count = 0
        total = len([actions for action in self.actions if action[0] is not ANNOTATE])
        try:
            for action, src, dst in self.actions:
                if action is not ANNOTATE:
                    count += 1
                    print("Action %2d(%2d): %s" % (count, total, ACTION_NAMES[action]))
                self.ACTION_METHODS[action](src, dst)
            print("BUILD DONE")
        except Exception as ex:
            print(str(ex))
            print("BUILD FAILED")
            sys.exit(1)

    def annotate(self, src, dst):
        self.print_header(src)

    def copyfile(self, src, dst):
        if src[0] == ARTIFACT:
            f = os.path.join(self.project_dir, self.get_artifact_src_name())
            t = os.path.join(self.artifact_dir, self.get_artifact_target_name())
        else:
            f = os.path.join(self.project_dir, *src)
            t = os.path.join(self.project_dir, *dst)
        self.print_src_dst(f, t)
        shutil.copyfile(f, t)

    def copydir(self, src, dst):
        f = os.path.join(self.project_dir, *src)
        t = os.path.join(self.project_dir, *dst)
        self.print_src_dst(f, t)
        shutil.copytree(f, t)

    def runpyscript(self, src, arg):
        try:
            script_path = os.path.join(self.project_dir, *src)
            self.print_src_dst(script_path, arg)
            if src[-1] == "setup.py":
                self.pushd(os.path.join(self.project_dir, "builddir"), None)
                success, msg = self.run_pyscript(script_path, [arg])
                self.popd(None, None)
            else:
                success, msg = self.run_pyscript(script_path, [self.project_dir, arg])
            if not success:
                raise Exception(msg)
        except Exception as ex:
            pass

    def runpytest(self, src, dst):
        script_path = os.path.join(self.project_dir, *src)
        self.pushd(os.path.dirname(script_path), None)
        self.print_src_dst(src, os.path.abspath(dst))
        success, msg = self.run_pyscript(script_path, [], display_stderr=True)
        if not success:
            raise Exception(msg)
        self.popd(None, None)

    def runcmd(self, src, dst):
        t = os.path.join(self.project_dir, *dst)
        self.pushd(os.path.dirname(t), None)
        self.print_src_dst(src, t)
        success, msg = self.run_command([src, t])
        self.popd(None, None)
        if not success:
            raise Exception(msg)

    def pushd(self, src, dst):
        self.print_src_dst(os.getcwd(), os.path.abspath(src))
        self.cwd = os.getcwd()
        os.chdir(src)

    def popd(self, src, dst):
        self.print_src_dst(None, self.cwd)
        print("    dst: %s" % self.cwd)
        os.chdir(self.cwd)

    def run_pyscript(self, script, args=[], display_stderr=False):
        return self.run_command(["python", script] + args, display_stderr)

    def run_command(self, cmd, display_stderr=False):
        if display_stderr:
            rc = subprocess.call(cmd)
            return rc == 0, ""
        else:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = p.communicate()
            print(out)
            if p.returncode == 0:
                return True, out[0]
            else:
                return False, out[1]

    def print_header(self, message):
        print("-------------------------------------------------------")
        print("  %s" % message)
        print("-------------------------------------------------------")

    def print_src_dst(self, src, dst):
        if src is not None:
            print("    src: %s" % src)
        if dst is not None:
            print("    dst: %s" % dst)

    def get_artifact_src_name(self):
        versionfile = os.path.join(self.project_dir, "source", "timelinelib", "meta", "version.py")
        f = open(versionfile, "r")
        text = f.read()
        lines = text.split("\n")
        for line in lines:
            if line[0:7] == "VERSION":
                break
        f.close()
        # VERSION = (0, 14, 0)
        line = line.split("(", 1)[1]
        line = line.split(")", 1)[0]
        major, minor, bug = line. split(", ")
        return "SetupTimeline%s%s%sPy2ExeWin32.exe" % (major, minor, bug)

    def get_artifact_target_name(self):
        return "%s-Win32Setup.exe" % self.archive.get_filename_version()


def main():
    artifactdir = os.path.join(sys.path[0], "..")
    Target("win32Installer").build(parse_arguments(), artifactdir)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", default="tip")
    return parser.parse_args()


if __name__ == "__main__":
    main()
