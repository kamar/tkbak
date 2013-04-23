#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#==================================================================================
#  Copyright:
#
#      Copyright (C) 2013 Konstas Marmatakis <marmako@gmail.com>
#
#   License:
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License version 3 as
#      published by the Free Software Foundation.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this package; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#==================================================================================

import locale
import gettext
import zipfile
import tarfile
import time
import os

from datetime import datetime, date
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
from tkinter.messagebox import askyesno, showinfo

from backup import backup

ALL = N+S+E+W

print(len(sys.argv), sys.argv[0])
abspath = os.path.abspath(sys.argv[0])
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)


glossa = locale.getdefaultlocale()[0]
print(glossa)

loc = locale.getlocale()
locale.setlocale(locale.LC_ALL, loc)

t = gettext.translation("tkbackup", localedir="locale", codeset='utf-8', fallback=True, \
                        languages=[glossa])
_ = t.gettext
t.install()



class GuiBackup:
    def __init__(self, parent=None, title=_('tkBackup Εφεδρικά Αντίγραφα')):
        self.parent = parent
        self.msg = StringVar()
        self.lis = []
#         self.minima = StringVar()
        self.typefile = StringVar()
        self.filemode = StringVar()
        self.title = title
        self.parent.title(title)
        self.makewidgets()
        self.parent.update_idletasks()
        self.center_window(self.parent)
        #Try to set icon.
        try:
            self.parent.iconbitmap('@images/wilber_painter.xbm')
        except:
            img = PhotoImage(file='docs/gplv3-88x31.gif')
            self.parent.tk.call('wm', 'iconphoto', root._w, img)
        self.parent.protocol("WM_DELETE_WINDOW", lambda: '')
        self.checkload()


    def center_window(self, afentiko):
        width = afentiko.winfo_width()
        height = afentiko.winfo_height()
        sw = afentiko.winfo_screenwidth()
        sh = afentiko.winfo_screenheight()
        afentiko.geometry("%dx%d%+d%+d" % (width, height, sw/2-width/2, sh/2-height/2))

    def makewidgets(self):
        frm = ttk.Frame(self.parent)
        frm.grid(row=0, column=0, sticky=ALL)

        btnlisf = ttk.Button(frm, text=_('Προσθήκη Αρχείων'), command=lambda: self.appendlis())
        btnlisf.grid(row=0, column=2, sticky=W)
        self.btnlisf = btnlisf
        btnlisd = ttk.Button(frm, text=_('Προσθήκη Φακέλων'), command=lambda: self.appendlis(2))
        btnlisd.grid(row=0, column=2)
        self.btnlisd = btnlisd
        btncopyr = ttk.Button(frm, text=_('Άδεια...'), command=showlicense)
        btncopyr.grid(row=0, column=2, sticky=E)
        loadbtn = ttk.Button(frm, text=_('Φόρτωση Προηγούμενων Αρχείων'), command=self.loadme)
        loadbtn.grid(row=0, column=0)
        self.loadbtn = loadbtn

        tex = ScrolledText(frm, width=70, height=20, bg='black', fg='green')
        tex.grid(row=1, column=2, rowspan=2, sticky=ALL)
        msg = _('Πρόγραμμα δημιουργίας εφεδρικών αντιγράφων')
        tex.insert(END, msg.center(70, '*'))
        self.tex = tex

        lblfrm1 = ttk.LabelFrame(frm, text=_('Αρχεία'))
        lblfrm1.grid(row=1, column=0, columnspan=2, sticky=ALL)
        lblfrm1.columnconfigure(0, weight=1)

        lboxfiles = Listbox(lblfrm1, width=40, height=10)
        lboxfiles.grid(row=0, column=0, sticky=ALL)
        self.lboxfiles = lboxfiles
        self.lboxfiles.bind('<Double-1>', self.OnDouble) #Να το παιδέψω.
        vsb01 = ttk.Scrollbar(lblfrm1, orient="vertical", command=self.lboxfiles.yview)
        self.lboxfiles.configure(yscrollcommand=vsb01.set)
        vsb01.grid(row=0, column=1, sticky=N+S)
#         btndel1 = ttk.Button(lblfrm1, text='Διαγραφή Επιλεγμένου', command=lambda: self.del_frm_list(None, self.lboxfiles))
#         btndel1.grid(sticky=S)

        lblfrm2 = ttk.LabelFrame(frm, text=_('Φάκελοι'))
        lblfrm2.grid(row=2, column=0, columnspan=2, sticky=ALL)
        lblfrm2.columnconfigure(0, weight=1)

        lboxdirs = Listbox(lblfrm2, width=40, height=10)
        lboxdirs.grid(row=0, column=0, stick=ALL)
        self.lboxdirs = lboxdirs
        self.lboxdirs.bind('<Double-1>', self.OnDouble)
        vsb = ttk.Scrollbar(lblfrm2, orient='vertical', command=self.lboxdirs.yview)
        self.lboxdirs.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky=N+S)
#         btndel2 = ttk.Button(lblfrm2, text='Διαγραφή Επιλεγμένου', command=lambda: self.del_frm_list(None, self.lboxdirs))
#         btndel2.grid(sticky=S)

        btnmnia = ttk.Button(frm, text=_('Μνεία'), command=self.credits)
        btnmnia.grid(row=0, column=3)


        lblfrmradio = ttk.LabelFrame(frm, text=_('Επιλογή Τύπου Αρχείου'))
        lblfrmradio.grid(row=1, column=3, sticky=N)

        rdiozip = ttk.Radiobutton(lblfrmradio, width=20, style="Toolbutton", text= _('Αρχείο Zip'), command=lambda:self.change_filename(self.ent.get()), variable=self.typefile, value='typezip')
        rdiozip.grid(row=0, column=0)

        rdiotar = ttk.Radiobutton(lblfrmradio, width=20,  style="Toolbutton", text=_('Αρχείο Tar'), command=lambda: self.change_filename(self.ent.get()),  variable=self.typefile, value='typetar')
        rdiotar.grid(row=1, column=0)

        self.typefile.set('typezip')

        lblfrmmode = ttk.Labelframe(frm, text=_('Άνοιγμα Αρχείου'))
        lblfrmmode.grid(row=1, column=3, sticky=S)

        rdioappend = ttk.Radiobutton(lblfrmmode, style="Toolbutton", text=_('για προσθήκη αρχείων και σχολίου'), variable=self.filemode, value='a')
        rdioappend.grid(row=0, column=0, sticky=W)

        rdiowrite = ttk.Radiobutton(lblfrmmode, style="Toolbutton", text=_('νέου για προσθήκη αρχείων'), variable=self.filemode, value='w')
        rdiowrite.grid(row=1, column=0, sticky=W)
#
#         rdiocomment = ttk.Radiobutton(lblfrmmode, style="Toolbutton", text=_('για προσθήκη σχολίου'), variable=self.filemode, value='a')
#         rdiocomment.grid(row=2, column=0, sticky=W)
#
        self.filemode.set('w')
        ent = ttk.Entry(frm)
        ent.grid(row=4, column=0, sticky=W+E)
        ent.insert(0, os.path.normpath(os.path.join(os.path.expanduser('~'),'zip.zip')))
        self.ent = ent

        defaultchk = ttk.Checkbutton(frm, text=_('Τελευταίο Αρχείο'), state=DISABLED, command='')
        defaultchk.grid(row=1, column=3, sticky=W+E)

        sp1 = ttk.Separator(frm)
        sp1.grid(row=3, column=0, columnspan=4, sticky=W+E)

        lbl = ttk.Label(frm, textvariable = self.msg)
        lbl.grid(row=4, column=2, sticky=N+S+W+E)

        sp2 = ttk.Separator(frm)
        sp2.grid(row=5, column=0, columnspan=4, sticky=W+E)

        lblcomment = ttk.Label(frm, text = _('Γράψτε το σχόλιό σας:'))
        lblcomment.grid(row=6, column=0, sticky=W)

        entcomment = ttk.Entry(frm, width=40)
        entcomment.grid(row=6, column=1, columnspan=2, sticky=W)
        self.entcomment = entcomment

        impfilebtn = ttk.Button(frm, text=_("Αρχείο Προορισμού"), command= self.impfile)
        impfilebtn.grid(row=7, column=0, sticky=W+E)
        self.impfilebtn =impfilebtn

        strtbtn = ttk.Button(frm, text=_('Ξεκίνα'), command=self.run_script)
        strtbtn.grid(row=7, column=2, sticky=W)
        self.strtbtn = strtbtn

        btnrestore = ttk.Button(frm, text=_('Επαναφορά Αντιγράφου'), command=self.restoreform)
        btnrestore.grid(row=7, column=2)
        self.btnrestore = btnrestore

        clsbtn = ttk.Button(frm, text=_('Κλείσιμο'), command=self.closeme)
        clsbtn.grid(row=7, column=2, sticky=E)
        self.clsbtn = clsbtn

        for child in frm.winfo_children():
            child.grid_configure(pady=3, padx=3)

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        for x in range(frm.grid_size()[0]-1):
            frm.columnconfigure(x, weight=1)
        for x in range(frm.grid_size()[1]-1):
            frm.rowconfigure(x,weight=1)

        #self.parent.update_idletasks()

    def credits(self):
        rtk = Toplevel()
        rtk.wm_attributes('-topmost', 1)
        n = ttk.Notebook(rtk)
        n.grid(row=0, column=0)
        frm1 = ttk.Frame(n)
        frm1.grid()
        frm2 = ttk.Frame(n)
        frm2.grid()
        frm3 = ttk.Frame(n)
        frm3.grid(sticky=ALL)
        frm3.rowconfigure(0, weight=1)
        frm3.columnconfigure(0, weight=1)

        n.add(frm1, text=_('Προγραμματισμός'))
        n.add(frm2, text=_('Μετάφραση'))
        n.insert(0, frm3, text=_('Περί'))
        n.select(0)
        n.enable_traversal()

        txtauthors = Text(frm1, width=45, height=10, bg='black', fg='green')
        txtauthors.grid()
        txtauthors.insert(END, open('AUTHORS').read())
        txtauthors['state'] = DISABLED

        txttranslators = Text(frm2, width=45, height=10, bg='black', fg='green')
        txttranslators.insert(END,  open('TRANSLATORS').read())
        txttranslators.grid()
        txttranslators['state'] = DISABLED

        style = ttk.Style()
        style.configure("f.TLabel", font=('Arial', 18, 'bold'), foreground='green', background='black')
        lblperi = ttk.Label(frm3, anchor=CENTER, style="f.TLabel")
        lblperi.grid(sticky=ALL)
        lblperi['text'] = 'tkBackup ' + open('VERSION').read()

        btnclose = ttk.Button(rtk, text=_('Κλείσιμο'), command=rtk.destroy)
        btnclose.grid(row=1, column=0)

        for child in rtk.winfo_children():
            child.grid_configure(pady=3, padx=3)
        rtk.protocol("WM_DELETE_WINDOW", lambda: '')
        rtk.resizable(0, 0)
        rtk.update_idletasks()
        self.center_window(rtk)
        rtk.wait_window()

    def change_filename(self, file , expand=True):
        dirpath, filename = os.path.split(file)
        if self.typefile.get() == 'typezip':
            file = filename.split('.')[0] + '.zip'
            if expand == True:
                self.ent.delete(0, END)
                self. ent.insert(0, os.path.normpath(os.path.join(dirpath, file)))
            else:
                return file
        else:
            file = filename.split('.')[0]  + '.tar.gz'
            if expand == True:
                self.ent.delete(0, END)
                self. ent.insert(0, os.path.normpath(os.path.join(dirpath, file)))
            else:
                return file

    def run_script(self):
        sys.stdout = self
        self.changestate()
        dt = datetime.now()
        if len(self.entcomment.get()) > 0:
            thecomment = '{0}'.format(self.entcomment.get())
        else:
            thecomment = '{0}'.format(_('Δημιουργήθηκε την: ')+dt.strftime('%Y-%m-%d %H:%M:%S'))

        backup.Backup(filesdirs=self.lis, target=self.ent.get(), mode=self.filemode.get(), ftype=self.typefile.get(), \
                      addcom=thecomment)

        sys.stdout = sys.__stdout__

        self.create_recent_files(self.ent.get())
        self.changestate(True)

    def changestate(self, s=False):
        if s == False:
            self.strtbtn['state'] = DISABLED
            self.clsbtn['state'] = DISABLED
            self.loadbtn['state'] = DISABLED
            self.btnlisf['state'] = DISABLED
            self.btnlisd['state'] = DISABLED
            self.impfilebtn['state'] = DISABLED
            self.btnrestore['state'] = DISABLED
        else:
            self.clsbtn['state'] = NORMAL
            self.btnlisf['state'] = NORMAL
            self.btnlisd['state'] = NORMAL
            self.impfilebtn['state'] = NORMAL
            self.btnrestore['state'] = NORMAL

    def add_comm(self, myzipfile, cc):
            if zipfile.is_zipfile(myzipfile):
                z = zipfile.ZipFile(myzipfile, 'a')
                z.comment = cc
                z.close()
            else:
                self.write(_('Το αρχείο {0} δεν υποστηρίζει σχόλια.').format(myzipfile))


    def del_frm_list(self, event, lboxname):
        items = lboxname.curselection()
        pos = 0
        for i in items :
            idx = int(i) - pos
            print(lboxname.get(idx))
            self.lis.remove(lboxname.get(idx))
            lboxname.delete( idx,idx )
            pos = pos + 1

    def OnDouble(self, event):
        widget = event.widget
        selection=widget.curselection()
        val = widget.get(selection[0])
        print(_("επιλογή:"), selection, ": '%s'" % val)
        if askyesno(self.title, _('Να διαγραφεί το επιλεγμένο στοιχείο {0};').format(val), default='yes') == True:
                    widget.delete(selection)
                    self.lis.remove(val)
##        print(self.lis)

    def write(self, minima):
        self.tex.insert(END, minima)
        self.tex.see(END)
        self.tex.update()
        try:
            self.msg.set(minima[:-1])
        except:
            pass

    def appendlis(self, fileordir=1):
        if fileordir == 1:
            p = os.path.normpath(askopenfilename())
            if not p in self.lis:
##                p = os.path.normpath(p)
                self.lis.append(p)
                self.lboxfiles.insert(END, p)

        elif fileordir == 2:
            p = os.path.normpath(askdirectory())
            if not p in self.lis:
                p = os.path.normpath(p)
                self.lis.append(p)
                self.lboxdirs.insert(END, p)


    def loadme(self):
        if askyesno(parent=self.parent, title=self.title, message=_('Να φορτωθούν τα προηγούμενα πηγαία αρχεία και φάκελοι;'), default='yes') == True:
            p = self.create_dirs()
            self.loadbtn['state'] = DISABLED
            try:
                if os.path.exists(os.path.join(p, 'files.txt')):
                    fp = open(os.path.join(p, 'files.txt'), 'r')
                    text = fp.read()
                    text = text.rstrip('\n')
                    text = text.lstrip('\n')
                    l1 = text.split('\n')

                    for item in l1:
                        self.lboxfiles.insert(END, item)
                        self.lis.append(item)
            except:
                self.tex.insert(END, _('Δεν υπάρχουν αποθηκευμένα αρχεία.') +'\n')
                self.tex.update()
            finally:
                try:
                    fp.close()
                except:
                    pass
            try:
                if os.path.exists(os.path.join(p, 'dirs.txt')):
                    fp1 = open(os.path.join(p, 'dirs.txt'), 'r')
                    text1 = fp1.read()
                    text1 = text1.rstrip('\n')
                    text1 = text1.lstrip('\n')
                    l2 = text1.split('\n')
                    for item in l2:
                        self.lboxdirs.insert(END, item)
                        self.lis.append(item)
            except:
                self.tex.insert(END, _('Δεν υπάρχουν αποθηκευμένοι φάκελοι.') + '\n')
                self.tex.update()
            finally:
                try:
                    fp1.close()
                except:
                    pass

    def create_dirs(self):

        if sys.platform.startswith('win') or sys.platform.endswith('NT'):
            the_path = os.path.normpath(os.environ['APPDATA']+os.sep+'.tkbackup')
        else:
            the_path = os.path.normpath(os.path.expanduser('~') + os.sep + '.tkbackup')

        if not os.path.exists(the_path):
            os.mkdir(the_path)
        return the_path

    def impfile(self):
        dumpfile =  self.change_filename(time.strftime('%Y%m%d') + '_' + time.strftime('%H%M%S'), False)

        p = asksaveasfilename(parent=self.parent, initialdir=os.path.expanduser('~'), initialfile=dumpfile)
        p = os.path.normpath(p)
        self.ent.delete(0, END)
        self.ent.insert(0, p)
##        self.create_recent_files(p)

    def create_recent_files(self, f):
        p = self.create_dirs()
        f = os.path.normpath(f)
        lfiles = []
        thefile = os.path.join(p, 'recent_backup_files.txt')
        if os.path.exists(thefile):
            fp = open(thefile, 'r', encoding='utf-8')
            text = fp.read()
            fp.close()
            text = text[:-1]
            fp = open(thefile, 'w', encoding='utf-8')
            for item in text.split('\n'):
                fp.write(item+'\n')
                if not item in lfiles:
                    lfiles.append(item)

            if not f in lfiles:
                lfiles.append(f)
                fp.write(f +'\n')
        else:
            fp = open(thefile, 'w', encoding='utf-8')
            fp.write(f +'\n')
            lfiles.append(f)
        fp.close()
        print(lfiles)
        return lfiles


    def checkload(self):
        p = self.create_dirs()
        fil1 = os.path.join(p, 'files.txt')
        fil2 = os.path.join(p, 'dirs.txt')
        try:
            text = open(fil1).read()
            if len(text.strip('\n')) == 0:
                os.unlink(fil1)
        except:
            pass
        try:
            text = open(fil2).read()
            if len(text.strip('\n')) == 0:
                os.unlink(fil2)
        except:
            pass

        check1 = os.path.exists(fil1)
        check2 = os.path.exists(fil2)

        if not check1 and not check2:
            self.loadbtn['state'] = DISABLED

    def closeme(self):
        if len(self.lis)> 0:
            answer = askyesno(title=self.title, message=_('Να σωθούν τα πηγαία αρχεία και οι φάκελοι για μελλοντική χρήση;'), default='yes')
            if answer == True:
                p = os.path.normpath(self.create_dirs())
                fname = os.path.join(p, 'files.txt')
                try:
                    fp = open(fname, 'w', encoding='utf-8')
                    l = self.lboxfiles.get(0, END)
                    for item in l:
                        fp.write(item+'\n')
                        self.tex.insert(END, _('Γράφω το αρχείο: {0}{1}').format(item, '\n'))
                        self.tex.update()
                except:
                    pass
                finally:
                    fp.close()

                try:
                    f = os.path.join(p, 'dirs.txt')
                    fp = open(f, 'w', encoding='utf-8')
                    l2 = self.lboxdirs.get(0, END)
                    for item in l2:
                        fp.write(item +'\n')
                        self.tex.insert(END, _('Γράφω τον κατάλογο: {0}{1}').format(item, '\n'))
                        self.tex.update()
                except:
                    pass
                finally:
                    fp.close()

        self.tex.insert(END, _('Τέλος.'))
        self.tex.insert(END, '\n')
        self.tex.insert(END, _('Γεια σας!!!'))
        self.tex.update()
        time.sleep(1)
        self.parent.destroy()

    def restoreform(self):
        self.parent.withdraw()
        master = Toplevel()
        gr = GuiRestore(master)
        gr.parent.wait_window()
        self.parent.deiconify()
        del gr

def showlicense():

    copyrightfile = 'docs/gpl-3.0.txt'

    root04 = Toplevel()
    root04.title(_('Άδεια...'))
    root04.resizable(0, 0)
    try:
        root04.attributes("-toolwindow", 1)
    except:
        root04.overrideredirect(1)

    def keyenter(event):
        root04.destroy()

    fh = open(copyrightfile, 'r')
    msg = fh.read()
    fh.close()

    kentrikoframe = ttk.Frame(root04)
    kentrikoframe.grid(column=0, row=0, sticky=(N, W, S, E))
    kentrikoframe.columnconfigure(0, weight=1)
    kentrikoframe.rowconfigure(0, weight=1)

    t=  ScrolledText(kentrikoframe, height=38, width=75, bg='#d9d9d9', relief=FLAT)
    t.grid(column=0, row=0, sticky=(N,S,W,E))
    t.insert(1.0, msg)
#     t.insert(END, '\n')
    t.configure(state=DISABLED)


    koumpi=ttk.Button(kentrikoframe, text=_('Κλείσιμο'), command=root04.destroy)
    koumpi.grid(column =0, row=1, sticky=E)
    koumpi.bind('<Return>', keyenter)

    for child in kentrikoframe.winfo_children():
        child.grid_configure(padx=2, pady=2)

    root04.update_idletasks()
    screen_width=root04.winfo_screenwidth()
    screen_hight=root04.winfo_screenheight()
    w = root04.winfo_width()
    h = root04.winfo_height()
    root04.geometry("%dx%d%+d%+d" % (w, h, (screen_width-w)/2, (screen_hight-h)/2))
    root04.grab_set()
    root04.focus_set()
    koumpi.focus()
    root04.wait_window()

class GuiRestore(GuiBackup):
    def __init__(self, parent=None, title=_('tkbackup Επαναφορά Εφεδρικών Αντιγράφων')):
        self.parent = parent
        self.title = title
        self.parent.title = self.title
        self.lis = []
        self.minima = StringVar()
        self.sxolio = StringVar()
        self.makewidgets()
        self.parent.update_idletasks()
        self.center_window(self.parent)
        self.parent.protocol("WM_DELETE_WINDOW", lambda: '')


    def makewidgets(self):
        frm = ttk.Frame(self.parent)
        frm.grid(row=0, column=0, sticky=ALL)
        #frm.config(bg='black')

        lblcomment = ttk.Label(frm, textvariable=self.sxolio)
        lblcomment.grid(row=0, column=0, columnspan=3, sticky=W+E)
        lstboxfromzip = Listbox(frm, width=50, height=24)
        lstboxfromzip.grid(row=1, column=0, sticky=ALL)
        lstboxfromzip.bind('<Double-1>', self.OnDouble)
        self.lstboxfromzip = lstboxfromzip
        vscbar = ttk.Scrollbar(frm, orient="vertical", command=self.lstboxfromzip.yview)
        self.lstboxfromzip.configure(yscrollcommand=vscbar.set)
        vscbar.grid(row=1, column=0, sticky=E+N+S)
        lstboxtorestore = Listbox(frm, width=50, height=24)
        lstboxtorestore.grid(row=1, column=1, sticky=ALL)
        self.lstboxtorestore = lstboxtorestore
        vscbar01 = ttk.Scrollbar(frm, orient="vertical", command=self.lstboxtorestore.yview)
        self.lstboxtorestore.configure(yscrollcommand=vscbar01.set)
        vscbar01.grid(row=1, column=1, sticky=E+N+S)
        ent = ttk.Entry(frm, width=30)
        ent.grid(row=2, column=0,  sticky=W)
        self.ent = ent

        btnepanaforaolon = ttk.Button(frm, text=_('Όλα...'), state=DISABLED, command=self.movetorestore)
        btnepanaforaolon.grid(row=2, column=0, sticky=E)
        self.btnepanaforaolon = btnepanaforaolon

#         lblminima = ttk.Label(frm, textvariable=self.minima, width=30)
#         lblminima.grid(row=2, column=1, sticky=ALL)
#         self.lblminima = lblminima
        tex = ScrolledText(frm, width=50, height=3)
        tex.grid(row=2, column=1, sticky=ALL)
        self.tex = tex

        btnfindzip = ttk.Button(frm, text=_('Φόρτωση Συμπιεσμένου Αρχείου'), command= self.openthezip)
        btnfindzip.grid(row=3, column=0)
        self.btnfindzip = btnfindzip

        btnextract = ttk.Button(frm, state=DISABLED, text= _('Αποσυμπίεση'), command=self.extractfromzip)
        btnextract.grid(row=3, column=1)
        self.btnextract = btnextract

        btncloseme = ttk.Button(frm, text=_('Κλείσιμο'), command=self.parent.destroy)
        btncloseme.grid(row=3, column=1, sticky=E)
        self.parent.update_idletasks()

        for child in frm.winfo_children():
            child.grid_configure(pady=5, padx=5)


    def loadme(self, getthefile):
        #file = r'C:\Users\Konstas\zip.zip'
        if zipfile.is_zipfile(getthefile):
            myzip = zipfile.ZipFile(getthefile, 'r')

            for f in myzip.namelist():
                self.lstboxfromzip.insert(END, f)

            self.lstboxfromzip.select_set(0)
    #         self.myzip = myzip

            if len(myzip.comment) > 0:
                self.sxolio.set(myzip.comment.decode())
            #    for file in self.lis:
            #        print(file)
        elif tarfile.is_tarfile(getthefile):
            myzip = tarfile.open(getthefile, 'r')

            for f in myzip.getnames():
                self.lstboxfromzip.insert(END, f)

            self.lstboxfromzip.select_set(0)

        myzip.close()
        self.btnfindzip['state'] = DISABLED

    def movetorestore(self):
        for item in self.lstboxfromzip.get(0, END):

            self.lstboxfromzip.select_set(0)
            selection = self.lstboxfromzip.curselection()

            self.lstboxtorestore.insert(END, item)
            self.lis.append(item)

            self.lstboxfromzip.delete(selection[0])
            self.btnextract['state'] = NORMAL

    def OnDouble(self, event):
        widget = event.widget
        selection=widget.curselection()
        val = widget.get(selection[0])
        self.lstboxtorestore.insert(END, val)
        self.lis.append(val)
        widget.delete(selection[0])
        self.btnextract['state'] = NORMAL

    def openthezip(self):
        ft = [('ZIP', '.zip'),
              ('Tar.gz', 'tar.gz'),
              ('All Files', '*')]

        p = askopenfilename(parent=self.parent, initialdir=os.path.expanduser('~'), \
                              title=self.title, filetypes=ft)
        p = os.path.normpath(p)
        self.ent.delete(0, END)
        self.ent.insert(0, p)
        self.loadme(self.ent.get())
        self.btnepanaforaolon['state'] = NORMAL

    def extractfromzip(self):
        sys.stdout = self
        extractdir = askdirectory(title=self.title)
        if askyesno(self.title, message= _('Επαναφορά στον κατάλογο: {0};').format(extractdir)) == True:
            backup.Restore(self.ent.get(), self.lis, extractdir)
            sys.stdout = sys.__stdout__
#             for file in self.lis:
#                 msg = _('Αποσυμπιέζω το: {0}').format(file)
#                 self.minima.set(msg)
#                 print(msg)
#                 self.myzip.extract(file, extractdir)
#         self.minima.set(self.myzip.comment.decode())
#         print(self.myzip.comment.decode())
#         self.myzip.close()
        self.btnextract['state'] = DISABLED


if __name__=='__main__':

    root = Tk()
    face = GuiBackup(root)
#     fc = GuiRestore(root)
    root.mainloop()
