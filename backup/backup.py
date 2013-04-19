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
import tarfile
import gettext
import locale
import time

glossa = locale.getdefaultlocale()[0]

t = gettext.translation("tkbackup", localedir="locale", codeset='utf-8', fallback=True, \
                        languages=[glossa])
_ = t.gettext
t.install()

def Backup(filesdirs=['/home/km/test', 'C:\\Python33'], target='zip_pyx.zip', ftype='typezip', mode='w', addcom=''):
    """Function that creats compressed files zip or tar.
    USAGE:
            Backup(filesdirs, target, ftype, mode, addcom)
    PARAMETERS:
            filesdirs: A list with the directories or files to be compressed.
            target: The full path and file name for the compressed file.
            ftype: The compressed file type. Possible arguments, 'typezip' or 'typetar'.
            mode: w for write, a for append, r for read.
            addcom: The comment for the zipfile. No comments allowed for tar."""
            
    count = 0
    target = target
    cdirs = filesdirs
    
    if ftype == 'typezip':
        
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
#         zip_command.close()
    
    elif ftype == 'typetar':
        mode = mode + ':gz'
        zip_command = tarfile.open(target, mode)

        if len(addcom) > 0:
            print(_('Δεν υπάρχει δυνατότητα εισαγωγής σχολίου.'))

        for cdir in cdirs:
            if os.path.isdir(cdir):
                for rt, dirs, files in os.walk(cdir):
                    for file in files:
                              
                        try:
                            minima = _('Συμπιέζω: ...{0}{1}').format(os.sep, file)
                            print(minima)
                            folder = os.path.join(rt, file)
                            folder = folder.replace(os.path.expanduser('~'), "")
                            zip_command.add(os.path.join(rt, file), arcname=folder)
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
                        
                    zip_command.add(os.path.normpath(cdir), arcname=folder)
                    count += 1
                except:
                    minima = _('Αποτυχία συμπίεσης του {0}').format(os.path.normpath(cdir))
                    print(minima)
                    pass
    print(_('Συμπιέστηκε το αρχείο {0}').format(target))
    zip_command.close()
    
    minima = _('Δημιουργήθηκε το αρχείο: {0}{1}').format(os.path.normpath(target), '\n')
    print(minima)

    minima = _('Συμπιέστηκαν συνολικά {0} αρχεία.{1}').format(count, '\n')
    print(minima)

def Restore(ziportar='', files=[], todirectory='.'):
    count = 0
    if zipfile.is_zipfile(ziportar) == True:
        print(_('Το αρχείο {0} είναι zip').format(ziportar))
        time.sleep(3)
        myzipfile = zipfile.ZipFile(ziportar, 'r')
        for file in files:
            msg = _('Αποσυμπιέζω το: {0}').format(file)
            print(msg)
            myzipfile.extract(file, todirectory)
            count += 1
        myzipfile.close()
    elif tarfile.is_tarfile(ziportar) == True:
        print(_('Το αρχείο {0} είναι tar').format(ziportar))
        time.sleep(3)
        myzipfile = tarfile.open(ziportar)
        for file in files:
            msg = _('Αποσυμπιέζω το: {0}').format(file)
            print(msg)
            myzipfile.extract(file, todirectory)
            count += 1
        myzipfile.close()
    else:
        print(_('Ο τύπος του αρχείου {0} δεν υποστηρ΄΄ίζεται.').format(ziportar))
    
    print(_('Αποσυμπιέστηκαν συνολικά {0} αρχεία από το αρχείο {1}.').format(count, ziportar))
        

if __name__ == '__main__':
    #Backup(addcom='Δημιουργήθηκε από τον ΚΜ.')
    Backup(target='tarf.tar.gz', mode='w', ftype='typetar')
