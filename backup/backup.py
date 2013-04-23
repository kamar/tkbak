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
import sys
import logging

glossa = locale.getdefaultlocale()[0]

t = gettext.translation("tkbackup", localedir="locale", codeset='utf-8', fallback=True, \
                        languages=[glossa])
_ = t.gettext
t.install()

def Backup(filesdirs=['/home/km/python', '/home/km/programming', r'C:\Users\Konstas\apodixispro'], target='zip_pyx.zip', ftype='typezip', mode='w', addcom='', silent=False):
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
            messagelog(_('Γράφω το σχόλιο: {0}').format(addcom), silent)
            zip_command.comment = addcom.encode()
        if len(filesdirs) == 0:
           messagelog
           messagelog(_('Δεν υπάρχουν αρχεία ή φάκελοι για συμπίεση.'), silent)
            #sys.exit(0)

        for cdir in cdirs:
            if os.path.isdir(cdir):
                for rt, dirs, files in os.walk(cdir):
                    for file in files:

                        try:
                            minima = _('Συμπιέζω: ...{0}{1}').format(os.sep, file)
                            messagelog(minima, silent)
                            folder = os.path.join(rt, file)
                            folder = folder.replace(os.path.expanduser('~'), "")
                            zip_command.write(os.path.join(rt, file), arcname=folder)
                            count += 1
                        except:
                            minima = _('Αποτυχία συμπίεσης του {0}').format(file)
                            messagelog(minima, silent)
                            pass

            elif os.path.isfile(cdir):
                try:
                    minima = _('Συμπιέζω: ...{0}').format(os.path.normpath(cdir))
                    messagelog(minima, silent)
                    folder = os.path.normpath(cdir)
                    folder = folder.replace(os.path.expanduser('~'), "")

                    zip_command.write(os.path.normpath(cdir), arcname=folder)
                    count += 1
                except:
                    minima = _('Αποτυχία συμπίεσης του {0}').format(os.path.normpath(cdir))
                    messagelog(minima, silent)
                    pass
#         zip_command.close()

    elif ftype == 'typetar':
        mode = mode + ':gz'
        zip_command = tarfile.open(target, mode)

        if len(addcom) > 0:
            messagelog(_('Δεν υπάρχει δυνατότητα εισαγωγής σχολίου.'), silent)

        for cdir in cdirs:
            if os.path.isdir(cdir):
                for rt, dirs, files in os.walk(cdir):
                    for file in files:

                        try:
                            minima = _('Συμπιέζω: ...{0}{1}').format(os.sep, file)
                            messagelog(minima, silent)
                            folder = os.path.join(rt, file)
                            folder = folder.replace(os.path.expanduser('~'), "")
                            zip_command.add(os.path.join(rt, file), arcname=folder)
                            count += 1
                        except:
                            minima = _('Αποτυχία συμπίεσης του {0}').format(file)
                            messagelog(minima, silent)
                            pass

            elif os.path.isfile(cdir):
                try:
                    minima = _('Συμπιέζω: ...{0}').format(os.path.normpath(cdir))
                    messagelog(minima, silent)
                    folder = os.path.normpath(cdir)
                    folder = folder.replace(os.path.expanduser('~'), "")

                    zip_command.add(os.path.normpath(cdir), arcname=folder)
                    count += 1
                except:
                    minima = _('Αποτυχία συμπίεσης του {0}').format(os.path.normpath(cdir))
                    messagelog(minima, silent)
                    pass
    messagelog(_('Συμπιέστηκε το αρχείο {0}').format(target), silent)
    zip_command.close()

    minima = _('Δημιουργήθηκε το αρχείο: {0}{1}').format(os.path.normpath(target), '\n')
    messagelog(minima, silent)

    minima = _('Συμπιέστηκαν συνολικά {0} αρχεία.{1}').format(count, '\n')
    messagelog(minima, silent)

def Restore(ziportar='', files=[], todirectory='.', silent=False):
    count = 0
    if zipfile.is_zipfile(ziportar) == True:
        messagelog(_('Το αρχείο {0} είναι zip').format(ziportar), silent)
        time.sleep(3)
        myzipfile = zipfile.ZipFile(ziportar, 'r')
        for file in files:
            msg = _('Αποσυμπιέζω το: {0}').format(file)
            messagelog(msg, silent)
            myzipfile.extract(file, todirectory)
            count += 1
        myzipfile.close()
    elif tarfile.is_tarfile(ziportar) == True:
        messagelog(_('Το αρχείο {0} είναι tar').format(ziportar), silent)
        time.sleep(3)
        myzipfile = tarfile.open(ziportar)
        for file in files:
            msg = _('Αποσυμπιέζω το: {0}').format(file)
            messagelog(msg, silent)
            myzipfile.extract(file, todirectory)
            count += 1
        myzipfile.close()
    else:
        messagelog(_('Ο τύπος του αρχείου {0} δεν υποστηρίζεται.').format(ziportar), silent)

    messagelog(_('Αποσυμπιέστηκαν συνολικά {0} αρχεία από το αρχείο {1}.').format(count, ziportar), silent)


def messagelog(msg, where):
    if where == False:
        print(msg)
    else:
        log_file = 'tkbackup.log'
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s ')
        logging.info(msg)
        logging.shutdown()


if __name__ == '__main__':
    Backup(addcom='Δημιουργήθηκε από τον ΚΜ.', silent=True)
    #Backup(target='tarf.tar.gz', mode='w', ftype='typetar')
