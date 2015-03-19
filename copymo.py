#!/usr/bin/env python3
#!-*- coding: utf-8 -*-

import os

os.chdir('po')
print(os.listdir('.'))
for file in os.listdir('.'):
    if file.endswith('.mo'):
        print(file)
        print(os.path.splitext(file)[0])
        cfile = open(file, 'rb').read()
        localedir = '../backup/locale/{0}/LC_MESSAGES'.format(os.path.splitext(file)[0])
        if os.path.exists(localedir):
            fh = open(os.path.join(localedir, 'tkbak.mo'), 'wb')
            fh.write(cfile)
        else:
            os.makedirs(localedir)
            fh = open(os.path.join(localedir, 'tkbak.mo'), 'wb')
            fh.write(cfile)
        try:
            fh.close()
        except:
            pass
