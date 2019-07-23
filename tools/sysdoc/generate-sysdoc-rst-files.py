#!/usr/bin/env python
#
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


import os


class Sysdoc(object):

    def create(self):
        root = os.path.join('..', '..', 'source')
        print('Source root dir: %s' % os.path.abspath(root))
        MARGIN = 13
        for root, dirs, files in os.walk(root):
            self.create_module_files(root, files, MARGIN)
            if '__init__.py' in files:
                self.create_package_file(root, dirs, files, MARGIN)
        MARGIN = 11
        root = os.path.join('..', '..', 'test', 'unit')
        for root, dirs, files in os.walk(root):
            self.create_module_files(root, files, MARGIN)
            if '__init__.py' in files:
                self.create_package_file(root, dirs, files, MARGIN)
        self.copy_files()

    def copy_files(self):
        for filename in ['index.rst', 'make.bat', 'Makefile', 'conf.py']:
            with open(filename) as f:
                text = f.read()
                path = os.path.join('..', '..', 'documentation', 'sysdoc', filename)
                with open(path, 'w') as dest:
                    dest.write(text)
                
    def create_module_files(self, root, files, margin):
        for file in [f for f in files if f.endswith('.py') and f != '__init__.py']:
            modname = file[:-3]
            rstfilename = "%s_%s" % (root[margin:].replace('\\', '_'), modname)
            module = root[margin:].replace('\\', '.') + '.%s' % modname
            self.create_module_file(module, rstfilename)

    def create_package_file(self, root, dirs, files, margin):
        modname = '%s' % root[margin:].replace('\\', '_')
        print(modname, root)
        dotted_modname = modname.replace('_', '.')
        rstfilename = '%s.rst' % root[margin:].replace('\\', '_')
        txt = []
        txt.append('package *%s*' % dotted_modname)
        txt.append('==========================================================================')
        txt.append(' ')
        txt.append('.. automodule:: %s' % dotted_modname)
        txt.append('   :members:')
        txt.append(' ')
        txt.append('.. toctree::')
        txt.append('   :maxdepth: 1')
        txt.append('   :caption: Modules:')
        txt.append(' ')
        for file in [f for f in files if f.endswith('.py') and f != '__init__.py']:
            txt.append('   %s_%s' % (modname, file[:-3]))
        txt.append(' ')
        txt.append('.. toctree::')
        txt.append('   :maxdepth: 1')
        txt.append('   :caption: Subpackages:')
        txt.append(' ')
        for dir in dirs:
            if not dir.endswith('__pycache__'):
                txt.append('   %s_%s' % (modname, dir))
        txt.append(' ')
        path = '..\\..\\documentation\\sysdoc\\%s.rst' % modname
        with open(path, 'w') as f:
            f.write('\n'.join(txt))
        print('packagefile', os.path.abspath(path))

    def create_module_file(self, module, filename):
        if module.startswith('.'):
            module = module[1:]
        if filename.startswith('_'):
            filename = filename[1:]
        path = '..\\..\\documentation\\sysdoc\\%s.rst' % filename
        print('modulefile', os.path.abspath(path))
        with open(path, 'w') as f:
            f.write(MODULE_TEMPLATE % (module, module))


MODULE_TEMPLATE = """\
module *%s*
====================================================================================================

.. automodule:: %s
    :members:
"""


print("Create sysdoc *.rst files. version 1.0")
Sysdoc().create()
