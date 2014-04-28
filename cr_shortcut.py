#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Only for windows"""

import os
import sys

import distutils.sysconfig

python_exe = os.path.join(distutils.sysconfig.EXEC_PREFIX, "pythonw.exe")

def create_app_shortcut(directory, filename, app):
    filename = os.path.join(directory, filename + ".lnk")
    icon = os.path.join(distutils.sysconfig.get_python_lib(), 'backup', 'docs', 'tkbackup.ico')
    app = os.path.join(sys.prefix, "scripts", app)
    create_shortcut(python_exe, "", filename, app, "", icon)
    file_created(filename)

def create_doc_shortcut(directory, filename, doc):
    filename = os.path.join(directory, filename + ".lnk")
    create_shortcut(doc, "", filename)
    file_created(filename)



if sys.argv[1] == '-install' or sys.argv[1] == 'install':
    
##    try:
##        os.rename(os.path.join(sys.prefix, 'Scripts', 'tkbak'),
##          os.path.join(sys.prefix, 'Scripts', 'tkbak.py'))
##        file_created(os.path.join(sys.prefix, 'Scripts', 'tkbak.py'))
##    except:
##        pass
#     copy_file('backup/docs/tkbackup.ico', os.path.join(distutils.sysconfig.get_python_lib(), 'backup', 'docs'))
#     file_created(os.path.join(distutils.sysconfig.get_python_lib(), 'backup', 'docs','tkbackup.ico'))
    try:
        try:
            desktop = get_special_folder_path("CSIDL_COMMON_DESKTOPDIRECTORY")
        except OSError:
            desktop =  get_special_folder_path("CSIDL_DESKTOPDIRECTORY")
    except OSError:
        pass

    try:
        try:
            startmenu = os.path.join(get_special_folder_path("CSIDL_COMMON_PROGRAMS"),
                                     'TkBackup') #"CSIDL_COMMON_STARTMENU"
        except OSError:
             startmenu = os.path.join(
                get_special_folder_path("CSIDL_PROGRAMS"),
                'TkBackup')

        try:
            os.mkdir(startmenu)
            directory_created(startmenu)
        except OSError:
            startmenu = None
    except OSError:
        pass


##    create_shortcut(os.path.join(sys.prefix, 'Scripts', 'tkbak.py'),
##                "Application for zip and archive files and directories.",
##                os.path.join(desktop, 'TkBackup.lnk'),
##                iconpath=os.path.join(distutils.sysconfig.get_python_lib(), 'backup', 'docs', 'tkbackup.ico'))
    try:
        create_app_shortcut(desktop, "TkBackup", os.path.join(sys.prefix, 'Scripts', 'tkbak'))
    except OSError:
        pass
##    file_created(os.path.join(desktop, 'TkBackup.lnk'))

##    create_shortcut(os.path.join(sys.prefix, 'Scripts', 'tkbak.py'),
##                "Application for zip and archive files and directories.",
##                os.path.join(startmenu, 'TkBackup.lnk'),
##                iconpath=os.path.join(distutils.sysconfig.get_python_lib(), 'backup', 'docs', 'tkbackup.ico'))
    try:
        create_app_shortcut(desktop, "TkBackup", os.path.join(sys.prefix, 'Scripts', 'tkbak'))
    except OSError:
        pass
##    file_created(os.path.join(startmenu, 'TkBackup.lnk'))

elif sys.argv[1] == '-remove':
    pass


    


