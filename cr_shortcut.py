#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Only for windows"""

import os
import sys

import distutils.sysconfig

if sys.argv[1] == '-install':
    
    os.rename(os.path.join(sys.prefix, 'Scripts', 'tkbak'),
          os.path.join(sys.prefix, 'Scripts', 'tkbak.py'))
    file_created(os.path.join(sys.prefix, 'Scripts', 'tkbak.py'))
    copy_file('backup/docs/tkbackup.ico', os.path.join(distutils.sysconfig.get_python_lib(), 'docs'))
    file_created(os.path.join(distutils.sysconfig.get_python_lib(), 'docs','tkbackup.ico'))
                 
    desktop = get_special_folder_path("CSIDL_COMMON_DESKTOPDIRECTORY")
    startmenu = get_special_folder_path("CSIDL_COMMON_STARTMENU")

    create_shortcut(os.path.join(sys.prefix, 'Scripts', 'tkbak.py'),
                "Application for zip and archive files and directories.",
                os.path.join(desktop, 'TkBackup.lnk'),
                '', '',
                os.path.join(distutils.sysconfig.get_python_lib(), 'docs', 'tkbackup.ico'))
    file_created(os.path.join(desktop, 'TkBackup.lnk'))

    create_shortcut(os.path.join(sys.prefix, 'Scripts', 'tkbak.py'),
                "Application for zip and archive files and directories.",
                os.path.join(startmenu, 'TkBackup.lnk'),
                '', '',
                os.path.join(distutils.sysconfig.get_python_lib(), 'docs', 'tkbackup.ico'))
    file_created(os.path.join(startmenu, 'TkBackup.lnk'))


    


