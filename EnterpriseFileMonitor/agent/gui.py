#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.26
#  in conjunction with Tcl version 8.6
#    Dec 31, 2019 02:08:27 PM CET  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import gui_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    gui_support.set_Tk_var()
    top = Toplevel1 (root)
    gui_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    gui_support.set_Tk_var()
    top = Toplevel1 (w)
    gui_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("878x137+503+154")
        top.minsize(148, 1)
        top.maxsize(1924, 1055)
        top.resizable(1, 1)
        top.title("Enterprise file change monitoring tool")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.MessageLabel = tk.Label(top)
        self.MessageLabel.place(relx=0.182, rely=0.073, height=26, width=286)
        self.MessageLabel.configure(activebackground="#f9f9f9")
        self.MessageLabel.configure(activeforeground="black")
        self.MessageLabel.configure(anchor='w')
        self.MessageLabel.configure(background="#d9d9d9")
        self.MessageLabel.configure(disabledforeground="#a3a3a3")
        self.MessageLabel.configure(foreground="#fd0000")
        self.MessageLabel.configure(highlightbackground="#d9d9d9")
        self.MessageLabel.configure(highlightcolor="black")

        self.NumberOfFilesLabel = tk.Label(top)
        self.NumberOfFilesLabel.place(relx=0.182, rely=0.219, height=26
                , width=141)
        self.NumberOfFilesLabel.configure(activebackground="#f9f9f9")
        self.NumberOfFilesLabel.configure(activeforeground="black")
        self.NumberOfFilesLabel.configure(anchor='w')
        self.NumberOfFilesLabel.configure(background="#d9d9d9")
        self.NumberOfFilesLabel.configure(disabledforeground="#a3a3a3")
        self.NumberOfFilesLabel.configure(foreground="#000000")
        self.NumberOfFilesLabel.configure(highlightbackground="#d9d9d9")
        self.NumberOfFilesLabel.configure(highlightcolor="black")
        self.NumberOfFilesLabel.configure(text='''NumberOfFilesLabel''')

        self.DirectoryEntry = tk.Entry(top)
        self.DirectoryEntry.place(relx=0.228, rely=0.73, height=24
                , relwidth=0.688)
        self.DirectoryEntry.configure(background="white")
        self.DirectoryEntry.configure(disabledforeground="#a3a3a3")
        self.DirectoryEntry.configure(font="TkFixedFont")
        self.DirectoryEntry.configure(foreground="#000000")
        self.DirectoryEntry.configure(highlightbackground="#d9d9d9")
        self.DirectoryEntry.configure(highlightcolor="black")
        self.DirectoryEntry.configure(insertbackground="black")
        self.DirectoryEntry.configure(selectbackground="#c4c4c4")
        self.DirectoryEntry.configure(selectforeground="black")
        self.DirectoryEntry.configure(textvariable=gui_support.monitoredDirectory)

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.011, rely=0.73, height=26, width=186)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Directory being monitored:''')

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.923, rely=0.73, height=23, width=61)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=gui_support.selectDirectory)
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Select...''')

        self.PercentageChangedLabel = tk.Label(top)
        self.PercentageChangedLabel.place(relx=0.182, rely=0.365, height=26
                , width=441)
        self.PercentageChangedLabel.configure(activebackground="#f9f9f9")
        self.PercentageChangedLabel.configure(activeforeground="black")
        self.PercentageChangedLabel.configure(anchor='w')
        self.PercentageChangedLabel.configure(background="#d9d9d9")
        self.PercentageChangedLabel.configure(disabledforeground="#a3a3a3")
        self.PercentageChangedLabel.configure(foreground="#000000")
        self.PercentageChangedLabel.configure(highlightbackground="#d9d9d9")
        self.PercentageChangedLabel.configure(highlightcolor="black")
        self.PercentageChangedLabel.configure(text='''PercentageChangedLabel''')

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.011, rely=0.073, height=26, width=147)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(anchor='e')
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Message:''')

        self.Label2_3 = tk.Label(top)
        self.Label2_3.place(relx=0.011, rely=0.219, height=26, width=147)
        self.Label2_3.configure(activebackground="#f9f9f9")
        self.Label2_3.configure(activeforeground="black")
        self.Label2_3.configure(anchor='e')
        self.Label2_3.configure(background="#d9d9d9")
        self.Label2_3.configure(disabledforeground="#a3a3a3")
        self.Label2_3.configure(foreground="#000000")
        self.Label2_3.configure(highlightbackground="#d9d9d9")
        self.Label2_3.configure(highlightcolor="black")
        self.Label2_3.configure(text='''Number of files:''')

        self.Label2_4 = tk.Label(top)
        self.Label2_4.place(relx=0.011, rely=0.365, height=26, width=147)
        self.Label2_4.configure(activebackground="#f9f9f9")
        self.Label2_4.configure(activeforeground="black")
        self.Label2_4.configure(anchor='e')
        self.Label2_4.configure(background="#d9d9d9")
        self.Label2_4.configure(disabledforeground="#a3a3a3")
        self.Label2_4.configure(foreground="#000000")
        self.Label2_4.configure(highlightbackground="#d9d9d9")
        self.Label2_4.configure(highlightcolor="black")
        self.Label2_4.configure(text='''Percentage changed:''')

        self.HostNameEntry = tk.Entry(top)
        self.HostNameEntry.place(relx=0.661, rely=0.073, height=24
                , relwidth=0.232)
        self.HostNameEntry.configure(background="white")
        self.HostNameEntry.configure(disabledforeground="#a3a3a3")
        self.HostNameEntry.configure(font="TkFixedFont")
        self.HostNameEntry.configure(foreground="#000000")
        self.HostNameEntry.configure(highlightbackground="#d9d9d9")
        self.HostNameEntry.configure(highlightcolor="black")
        self.HostNameEntry.configure(insertbackground="black")
        self.HostNameEntry.configure(selectbackground="#c4c4c4")
        self.HostNameEntry.configure(selectforeground="black")
        self.HostNameEntry.configure(textvariable=gui_support.sendToAddress)
        self.HostNameEntry.bind('<Key>',lambda e:gui_support.hostnameKeypress(e))

        self.Label2_5 = tk.Label(top)
        self.Label2_5.place(relx=0.513, rely=0.073, height=26, width=127)
        self.Label2_5.configure(activebackground="#f9f9f9")
        self.Label2_5.configure(activeforeground="black")
        self.Label2_5.configure(anchor='e')
        self.Label2_5.configure(background="#d9d9d9")
        self.Label2_5.configure(disabledforeground="#a3a3a3")
        self.Label2_5.configure(foreground="#000000")
        self.Label2_5.configure(highlightbackground="#d9d9d9")
        self.Label2_5.configure(highlightcolor="black")
        self.Label2_5.configure(text='''Send messages to:''')

        self.LatestLabel = tk.Label(top)
        self.LatestLabel.place(relx=0.182, rely=0.511, height=26, width=508)
        self.LatestLabel.configure(activebackground="#f9f9f9")
        self.LatestLabel.configure(activeforeground="black")
        self.LatestLabel.configure(anchor='w')
        self.LatestLabel.configure(background="#d9d9d9")
        self.LatestLabel.configure(disabledforeground="#a3a3a3")
        self.LatestLabel.configure(foreground="#000000")
        self.LatestLabel.configure(highlightbackground="#d9d9d9")
        self.LatestLabel.configure(highlightcolor="black")
        self.LatestLabel.configure(text='''LatestLabel''')

        self.Label2_1 = tk.Label(top)
        self.Label2_1.place(relx=0.011, rely=0.511, height=26, width=147)
        self.Label2_1.configure(activebackground="#f9f9f9")
        self.Label2_1.configure(activeforeground="black")
        self.Label2_1.configure(anchor='e')
        self.Label2_1.configure(background="#d9d9d9")
        self.Label2_1.configure(disabledforeground="#a3a3a3")
        self.Label2_1.configure(foreground="#000000")
        self.Label2_1.configure(highlightbackground="#d9d9d9")
        self.Label2_1.configure(highlightcolor="black")
        self.Label2_1.configure(text='''LatestChanges:''')

if __name__ == '__main__':
    vp_start_gui()




