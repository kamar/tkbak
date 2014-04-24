#!/usr/bin/env python3
# -*- coding: utf8 -*-
'''
Created on 18-11-2013
Updated on 24-04-2014
@ author: Konstas Marmatakis
'''

import os
import sys
from distutils.core import setup
from distutils.file_util import copy_file

files = ['docs/*', 'locale/el_GR/LC_MESSAGES/*']


setup(name='tkbackup',
      version=open('backup/docs/VERSION').read().strip(),
      description='Simple Backup Program',
      author='Konstas Marmatakis',
      author_email='marmako@gmail.com',
      url='https://bitbucket.org/kamar/tkbackup',
      packages=['backup'],
      scripts=['tkbak', 'cr_shortcut.py'],
      package_data = {'backup': files},
      license='GNU/GPLv3',
#       data_files=[('docs', ['docs/gpl-3.0.txt', 'AUTHORS', 'README.rst', 'TRANSLATORS', 'VERSION']),
#                   ('images', ['docs/gplv3-127x51.gif', 'docs/gplv3-127x51.png',
#                               'docs/gplv3-88x31.gif', 'docs/gplv3-88x31.png', 
#                               'docs/tkbackup.gif', 'docs/tkbackup.png'])],
      long_description=open('backup/docs/README.rst').read(),
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: X11 Applications',
                   'Intended Audience :: Other Audience',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Operating System :: Microsoft',
                   'Operating System :: Microsoft :: Windows :: Windows 7',
                   'Operating System :: POSIX',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   'Topic :: Desktop Environment',
                   'Topic :: System :: Archiving :: Backup']
      )

if sys.argv[1] == 'install':
    if os.name == 'posix':
        copy_file('tkbackup.desktop', '/usr/share/applications/')
        copy_file('backup/docs/tkbackup.png', '/usr/share/icons/hicolor/48x48/apps/')
