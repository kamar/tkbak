#!/usr/bin/env python3
# encoding: utf-8
'''
backup -- shortdesc

backup is a description

It defines classes_and_methods

@author:     user_name
            
@copyright:  2013 organization_name. All rights reserved.
            
@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import os
import zipfile
import gettext
import locale

glossa = locale.getdefaultlocale()[0]

t = gettext.translation("tkbackup", localedir="locale", codeset='utf-8', fallback=True, \
                        languages=[glossa])
_ = t.gettext
t.install()

def Backup(filesdirs=[r'C:\Python33'], target='zip_pyx.zip', mode='w', addcom=''):
    _("""Δοκιμή για το πρόγραμμα.""")
    count = 0
    target = target
    cdirs = filesdirs
    
    zip_command = zipfile.ZipFile(target, mode)
    
    if len(addcom) > 0:
        print(_('Γράφω το σχόλιο: {0}').format(addcom))
        zip_command.comment = addcom.encode()
    
    for cdir in cdirs:
        if os.path.isdir(cdir):
            for rt, dirs, files in os.walk(cdir):
                for file in files:
                              
                    try:
                        minima = _('Συμπιέζω: ...{0}{1}').format(os.sep, file)
                        print(minima)
                        folder = os.path.join(rt, file)
                        folder = folder.replace(os.path.expanduser('~'), "")
                        zip_command.write(os.path.join(rt, file), arcname=folder)
                        count += 1
                    except:
                        minima = _('Αποτυχία συμπίεσης του {0}').format(file)
                        pass
                    
        elif os.path.isfile(cdir):
            try:
                minima = _('Συμπιέζω: ...{0}').format(os.path.normpath(cdir))
                print(minima)
                folder = os.path.normpath(cdir)
                folder = folder.replace(os.path.expanduser('~'), "")
                        
                zip_command.write(os.path.normpath(cdir), arcname=folder)
                count += 1
            except:
                minima = _('Αποτυχία συμπίεσης του {0}').format(os.path.normpath(cdir))
                print(minima)
                pass          
                        

    zip_command.close()
    
    minima = _('Δημιουργήθηκε το αρχείο: {0}{1}').format(os.path.normpath(target), '\n')
    print(minima)

    minima = _('Συμπιέστηκαν συνολικά {0} αρχεία.{1}').format(count, '\n')
    print(minima)

if __name__ == '__main__':
    Backup(addcom='Δημιουργήθηκε από τον ΚΜ.')
