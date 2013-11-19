#!/usr/bin/env python3
# -*- coding: utf8 -*-
'''
Created on 18 Νοε 2013

@author: Konstas
'''
from distutils.core import setup

setup(name='tkbackup',
      version=open('VERSION').read().strip(),
      description='Simple Backup Program',
      author='Konstas Marmatakis',
      author_email='marmako@gmail.com',
      url='https://bitbucket.org/kamar/tkbackup',
      packages=['backup'],
      scripts=['tkbackup'],
      license='GNU/GPLv3',
      data_files=[('docs', ['docs/gpl-3.0.txt', 'AUTHORS', 'README.rst', 'TRANSLATORS', 'VERSION']),
                  ('images', ['docs/gplv3-127x51.gif', 'docs/gplv3-127x51.png',
                              'docs/gplv3-88x31.gif', 'docs/gplv3-88x31.png', 
                              'docs/tkbackup.gif', 'docs/tkbackup.png'])],
      long_description=open('README.rst').read(),
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