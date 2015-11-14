# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014, 2015  Rickard Lindberg, Roger Lindberg
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

COPYFILE = 0
COPYDIR = 1
MAKEDIR = 2
PUSHD = 3
POPD = 4
RUNCMD = 5
RUNPYSCRIPT = 6
CPYDIR = 7
ANNOTATE = 8
RUNPYTEST = 9

ACTION_NAMES = {COPYFILE: "COPYFILE",
                COPYDIR: "COPYDIR",
                MAKEDIR: "MAKEDIR",
                PUSHD: "PUSHD",
                POPD: "POPD",
                RUNCMD: "RUNCMD",
                RUNPYSCRIPT: "RUNPYSCRIPT",
                RUNPYTEST: "RUNPYTEST",
                CPYDIR: "CPYDIR", }


known_targets = ("win32")


win32_actions = ((ANNOTATE, "Modify some python files", ""),
                 #(RUNPYSCRIPT, ["tools", "winbuildtools", "mod_timeline_py.py"], ""),
                 #(RUNPYSCRIPT, ["tools", "winbuildtools", "mod_paths_py.py"], ""),
                 #(RUNPYSCRIPT, ["tools", "winbuildtools", "mod_version_py.py"], ""),
                 #(RUNPYSCRIPT, ["tools", "winbuildtools", "mod_factory_py.py"], ""),
                 #(RUNPYSCRIPT, ["tools", "winbuildtools", "mod_timeline_iss_win32.py"], ""),

                 (ANNOTATE, "Run Tests", ""),
                 #(RUNPYTEST, ["test", "execute-specs.py"], ""),

                 (ANNOTATE, "Create distribution directory", ""),
                 (RUNPYSCRIPT, ["release", "win", "inno", "setup.py"], "py2exe"),

                 #(ANNOTATE, "Create distribution executable", ""),
                 #(COPYDIR, "translations", "translations"),
                 #(RUNCMD, "python", r"translations\generate-mo-files.py"),
                 #(CPYDIR, "translations", r"dist\translations"),
                 #(COPYDIR, "icons", r"dist\icons"),
                 #(COPYFILE, r"release\win\inno\Timeline.ico", r"dist\icons\Timeline.ico"),
                 #(COPYFILE, "COPYING", "COPYING"),
                 #(COPYFILE, r"release\win\inno\WINSTALL", r"WINSTALL"),

                 #(ANNOTATE, "Create Setup executable", ""),
                 #(RUNCMD, "iscc.exe", r"inno\timelineWin32_2.iss"),

                 (ANNOTATE, "Done", ""),
                 )


actions = {"win32": win32_actions}


class Target():

    def __init__(self, target):
        print "-------------------------------------------------------"
        print "  %s" % ("Building target %s" % target)
        print "-------------------------------------------------------"
        self.target = target
        self.actions = actions[target]
        self.ACTION_METHODS = {COPYFILE: self.copyfile,
                               COPYDIR: self.copydir,
                               MAKEDIR: self.makedir,
                               PUSHD: self.pushd,
                               POPD: self.popd,
                               RUNCMD: self.runcmd,
                               RUNPYSCRIPT: self.runpyscript,
                               RUNPYTEST: self.runpytest,
                               CPYDIR: self.cpydir,
                               ANNOTATE: self.annotate}

    def build(self, arguments, artifact_dir, temp_dir):
        self.artifact_dir = artifact_dir
        self.project_dir = self.create_project_dir(arguments, temp_dir)
        print "Artifact dir: %s" % self.artifact_dir
        print "Project dir:  %s" % self.project_dir
        print "Working dir:  %s" % os.getcwd()
        self.execute_actions()

    def create_project_dir(self, arguments, temp_dir):
        print "Creating project directory"
        repository = timelinetools.packaging.repository.Repository()
        archive = repository.archive(arguments.revision, temp_dir, ARCHIVE)
        return os.path.join(temp_dir, ARCHIVE)

    def execute_actions(self):
        count = 0
        total = len([actions for action in self.actions if action[0] is not ANNOTATE])
        try:
            for action, src, dst in self.actions:
                if action is not ANNOTATE:
                    count += 1
                    print "Action %2d(%2d): %s" % (count, total, ACTION_NAMES[action])
                self.ACTION_METHODS[action](src, dst)
            print "BUILD DONE"
        except Exception, ex:
            print str(ex)
            print "BUILD FAILED"
            sys.exit(1)

    def annotate(self, src, dst):
        self.print_header(src)

    def copyfile(self, src, dst):
        self.print_src_dst(src, os.path.abspath(dst))
        shutil.copyfile(os.path.join(self.timeline_dir, src), dst)

    def copydir(self, src, dst):
        self.print_src_dst(src, os.path.abspath(dst))
        shutil.copytree(os.path.join(self.timeline_dir, src), os.path.join(dst))

    def cpydir(self, src, dst):
        self.print_src_dst(src, os.path.abspath(dst))
        shutil.copytree(os.path.join(src), os.path.join(dst))

    def makedir(self, src, dst):
        self.print_src_dst(None, dst)
        print "    dst: %s" % os.path.abspath(dst)
        os.mkdir(os.path.join(self.target_dir, dst))

    def runpyscript(self, src, arg):
        try:
            script_path = os.path.join(self.project_dir, *src)
            self.print_src_dst(script_path, arg)
            if src[-1] == "setup.py":
                self.pushd(self.project_dir, None)
                print os.getcwd()
                success, msg = self.run_pyscript(script_path, [arg])
                self.popd(None, None)
            else:    
                success, msg = self.run_pyscript(script_path, [self.project_dir, arg])
            if not success:
                raise Exception(msg)
        except Exception, ex:
            pass

    def runpytest(self, src, dst):
        script_path = os.path.join(self.project_dir, *src)
        self.pushd(os.path.dirname(script_path), None)
        self.print_src_dst(src, os.path.abspath(dst))
        success, msg = self.run_pyscript(script_path, [dst], display_stderr=True)
        if not success:
            raise Exception(msg)
        self.popd(None, None)

    def runcmd(self, src, dst):
        self.print_src_dst(src, dst)
        success, msg = self.run_command([src, dst])
        if not success:
            raise Exception(msg)

    def pushd(self, src, dst):
        self.print_src_dst(os.getcwd(), os.path.abspath(src))
        self.cwd = os.getcwd()
        os.chdir(src)

    def popd(self, src, dst):
        self.print_src_dst(None, self.cwd)
        print "    dst: %s" % self.cwd
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
            print out
            if p.returncode == 0:
                return True, out[0]
            else:
                return False, out[1]

    def print_header(self, message):
        print "-------------------------------------------------------"
        print "  %s" % message
        print "-------------------------------------------------------"

    def print_src_dst(self, src, dst):
        if src is not None:
            print "    src: %s" % src
        if dst is not None:
            print "    dst: %s" % dst


def main():
    artifactdir = os.path.join(sys.path[0], "..")
    tempdir = tempfile.mkdtemp()
    try:
        Target("win32").build(parse_arguments(), artifactdir, tempdir)
    finally:
        shutil.rmtree(tempdir)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", default="tip")
    return parser.parse_args()


if __name__ == "__main__":
    main()
