#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on 18-11-2013
Updated on 26-04-2014
@ author: Konstas Marmatakis
'''

import os
import sys
from distutils.core import setup
from distutils.sysconfig import EXEC_PREFIX
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
      long_description=open('backup/docs/README.rst', encoding='utf-8').read(),
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
        try:
            locations = open('RECORD', encoding='utf-8').read()
            # print(locations)
            for line in locations.splitlines():
                if line[-5:] == 'tkbak':
                    executable = line
        except:
            print('Can\'t read the location from the script.')                            
            locations='/usr/bin'
    
        txt ='#!/usr/bin/env xdg-open\n\n[Desktop Entry]\nVersion=1.0\nType=Application\nTerminal=false\nName[el_GR]=TkBackup\nExec={0}\nIcon={1}\nComment[el_GR]=Εφαρμογή για την δημιουργία και συμπίεση εφεδρικών αντιγράφων.\nComment=Application for zip and archive files and directories.\nName=TkBackup\nGenericName[el_GR]=TkBackup\nCategories=Utility\nTerminal=false\nStartupNotify=false\n'
        # copy_file('tkbackup.desktop', '/usr/share/applications/')
        copy_file('backup/docs/tkbackup.png', '/usr/share/icons/hicolor/48x48/apps/')
        try:
            print('Writing {0} ...'.format(os.path.join('/usr/share/applications', 'tkbackup.desktop')))
            fh = open(os.path.join('/usr/share/applications/', 'tkbackup.desktop'), 'w', encoding='utf-8')
            fh.write(txt.format((executable or os.path.join(EXEC_PREFIX, 'bin', 'tkbak')), os.path.join('/usr/share/icons/hicolor/48x48/apps', 'tkbackup.png')))
            fh.close()
        except:
            print('Error. Can\'t create {0}'.format(os.path.join('/usr/share/applications/', 'tkbackup.desktop')))
        finally:
            fh.close()
##    else:
##        os.rename(os.path.join(sys.prefix, 'Scripts', 'tkbak'),
##              os.path.join(sys.prefix, 'Scripts', 'tkbak.py'))
##        file_created(os.path.join(sys.prefix, 'Scripts', 'tkbak.py'))
##        copy_file('backup/docs/tkbackup.ico', os.path.join(sys.prefix, 'Icons'))
##        file_created(os.path.join(sys.prefix, 'Icons', 'tkbackup.ico'))
##                     
##        desktop = get_special_folder_path("CSIDL_COMMON_DESKTOPDIRECTORY")
##        startmenu = get_special_folder_path("CSIDL_COMMON_STARTMENU")
##
##        create_shortcut(os.path.join(sys.prefix, 'Scripts', 'tkbak.py'),
##                    "Application for zip and archive files and directories.",
##                    os.path.join(desktop, 'TkBackup.lnk'),
##                    '', '',
##                    os.path.join(sys.prefix, 'Icons', 'tkbackup.ico'))
##        file_created(os.path.join(desktop, 'TkBackup.lnk'))
##
##        create_shortcut(os.path.join(sys.prefix, 'Scripts', 'tkbak.py'),
##                    "Application for zip and archive files and directories.",
##                    os.path.join(startmenu, 'TkBackup.lnk'),
##                    '', '',
##                    os.path.join(sys.prefix, 'Icons', 'tkbackup.ico'))
##        file_created(os.path.join(startmenu, 'TkBackup.lnk'))
        
