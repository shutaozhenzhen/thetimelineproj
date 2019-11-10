#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
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


import argparse
import doctest
import os.path
import random
import sys
import unittest

from timelinetools.paths import ROOT_DIR
from timelinetools.paths import TEST_DIR


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", default=[], nargs="*")
    parser.add_argument("--halt-gui", default=False, action="store_true")
    parser.add_argument("--auto-close", default=False, action="store_true")
    parser.add_argument("--write-testlist", default=None)
    parser.add_argument("--read-testlist", default=None)
    parser.add_argument("-v", default=False, action="store_true")
    return parser.parse_args()


def execute_specs(arguments):
    setup_displayhook()
    setup_paths()
    install_gettext_in_builtin_namespace()
    setup_humblewx()
    set_halt_gui_flag(arguments)
    suite = create_suite(arguments)
    all_pass = execute_suite(suite, select_verbosity(arguments))
    return all_pass


def setup_displayhook():
    # Background why this is needed:
    # http://sheep.art.pl/Gettext%20and%20Doctest%20Together%20in%20Python
    # Current doctest seems to use sys.__displayhook__ instead, so replace both.
    def displayhook_that_does_not_modify_(value):
        if value is not None:
            print(repr(value))
    sys.__displayhook__ = sys.displayhook = displayhook_that_does_not_modify_


def setup_paths():
    sys.path.insert(0, os.path.join(ROOT_DIR, "source"))
    sys.path.insert(0, os.path.join(ROOT_DIR, "test"))


def install_gettext_in_builtin_namespace():
    def _(message):
        # Make sure to return a non-ascii symbol to ensure that the caller
        # handles the unicode object properly.
        return "⟪%s⟫" % message
    import builtins
    builtins.__dict__["_"] = _


def setup_humblewx():
    import timelinelib.wxgui.setup
    timelinelib.wxgui.setup.setup_humblewx()


def set_halt_gui_flag(arguments):
    from timelinelib.test.cases.unit import UnitTestCase
    UnitTestCase.HALT_GUI = arguments.halt_gui
    UnitTestCase.AUTO_CLOSE = arguments.auto_close


def create_include_test_function(arguments):
    if len(arguments.only) > 0:
        patterns = arguments.only
        return lambda test: any([pattern in test.id() for pattern in patterns])
    else:
        return lambda test: True


def create_suite(arguments):
    whole_suite = suite_from_modules(find_test_modules())
    if arguments.read_testlist:
        return read_testlist(arguments, whole_suite)
    else:
        return write_testlist(
            arguments,
            shuffled_suite(
                filter_suite(
                    whole_suite,
                    create_include_test_function(arguments)
                )
            )
        )
    return suite


def write_testlist(arguments, suite):
    if arguments.write_testlist:
        with open(arguments.write_testlist, "w") as f:
            for test in suite:
                f.write("{}\n".format(test.id()))
    return suite


def read_testlist(arguments, whole_suite):
    test_by_id = {}
    for test in extract_test_cases(whole_suite):
        test_by_id[test.id()] = test
    suite = unittest.TestSuite()
    with open(arguments.read_testlist) as f:
        for test_id in f:
            suite.addTest(test_by_id[test_id.strip()])
    return suite


def suite_from_modules(modules):
    suite = unittest.TestSuite()
    for (test_type, module) in modules:
        {
            "spec": load_test_cases_from_module_name,
            "doctest": load_doc_tests_from_module_name,
        }[test_type](suite, module)
    return suite


def load_test_cases_from_module_name(suite, module_name):
    __import__(module_name)
    module = sys.modules[module_name]
    module_suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    suite.addTest(module_suite)


def load_doc_tests_from_module_name(suite, module_name):
    __import__(module_name)
    module = sys.modules[module_name]
    try:
        module_suite = doctest.DocTestSuite(module)
    except ValueError:
        # No tests found
        pass
    else:
        suite.addTest(module_suite)


def find_test_modules():
    modules = find_specs("specs") + find_specs("unit") + find_specs("lint") + find_doctests()
    random.shuffle(modules)
    return modules


def find_specs(subdir):
    specs = []
    for file in os.listdir(os.path.join(TEST_DIR, subdir)):
        if os.path.isdir(os.path.join(TEST_DIR, subdir, file)):
            specs.extend(find_specs(os.path.join(subdir, file)))
        elif file.endswith(".py") and file != "__init__.py":
            module_name = os.path.basename(file)[:-3]
            abs_module_name = "%s.%s" % (subdir.replace(os.sep, "."), module_name)
            specs.append(("spec", abs_module_name))
    return specs


def find_doctests():
    doctests = []
    timelinelib_dir = os.path.join(ROOT_DIR, "source", "timelinelib")
    for module in find_python_modules(timelinelib_dir):
        doctests.append(("doctest", module))
    return doctests


def find_python_modules(path):
    module_names = []
    files = os.listdir(path)
    if "__init__.py" in files:
        module_names.append("%s" % os.path.basename(path))
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_names.append("%s.%s" % (os.path.basename(path), file[:-3]))
            if os.path.isdir(os.path.join(path, file)):
                for x in find_python_modules(os.path.join(path, file)):
                    module_names.append("%s.%s" % (os.path.basename(path), x))
    return module_names


def filter_suite(test, include_test_function):
    new_suite = unittest.TestSuite()
    if isinstance(test, unittest.TestCase):
        if include_test_function(test):
            new_suite.addTest(test)
    else:
        for subtest in test:
            new_suite.addTest(filter_suite(subtest, include_test_function))
    return new_suite


def shuffled_suite(suite):
    test_cases = extract_test_cases(suite)
    random.shuffle(test_cases)
    return unittest.TestSuite(test_cases)


def extract_test_cases(suite):
    if isinstance(suite, unittest.TestCase):
        return [suite]
    else:
        tests = []
        for test in suite:
            tests.extend(extract_test_cases(test))
        return tests


def execute_suite(suite, verbosity):
    res = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return res.wasSuccessful()


def select_verbosity(arguments):
    if len(arguments.only) > 0 or arguments.v:
        return 2
    else:
        return 1


if __name__ == '__main__':
    all_pass = execute_specs(parse_arguments())
    if all_pass:
        sys.exit(0)
    else:
        sys.exit(1)
