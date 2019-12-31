#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.26
#  in conjunction with Tcl version 8.6
#    Dec 28, 2019 04:45:04 PM CET  platform: Windows NT
#    Dec 28, 2019 05:44:38 PM CET  platform: Windows NT
#    Dec 29, 2019 07:09:48 PM CET  platform: Windows NT
#    Dec 30, 2019 01:35:02 PM CET  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
    import tkinter.filedialog

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import os
import watchdog.observers
import watchdog.events
import datetime
import threading
import messages
import socket
import pickle


class dirStatistics(watchdog.events.FileSystemEventHandler):
    def __init__(self, *args, history_periods = 24*60*60, **kwargs):
        self._nfCreated = 0
        self._nfMoved = 0
        self._nfDeleted = 0
        self._nfModified = 0
        self._created = []
        self._moved = []
        self._deleted = []
        self._modified = []
        self._timespan_seconds = history_periods
        self._lock = threading.Lock()
        return super().__init__(*args, **kwargs)
    def reset(self):
        with self._lock:
            self._nfCreated = 0
            self._nfMoved = 0
            self._nfDeleted = 0
            self._nfModified = 0
            self._created = []
            self._moved = []
            self._deleted = []
            self._modified = []

    def dispatch(self, event):
        """override dispatch event, count events"""
        with self._lock:
            self._nfCreated = self._nfCreated + 1 if event.event_type == watchdog.events.EVENT_TYPE_CREATED else self._nfCreated
            self._nfMoved = self._nfMoved + 1 if event.event_type == watchdog.events.EVENT_TYPE_MOVED else self._nfMoved
            self._nfDeleted = self._nfDeleted + 1 if event.event_type == watchdog.events.EVENT_TYPE_DELETED else self._nfDeleted
            self._nfModified = self._nfModified + 1 if event.event_type == watchdog.events.EVENT_TYPE_MODIFIED else self._nfModified
    def doStats(self):
        """to be called periodically with roughly constant interval time"""
        with self._lock:
            self._created.append(self._nfCreated)
            self._deleted.append(self._nfDeleted)
            self._modified.append(self._nfModified)
            self._moved.append(self._nfMoved)
            if len(self._created) > self._timespan_seconds:
                self._created.pop(0)
                self._deleted.pop(0)
                self._modified.pop(0)
                self._moved.pop(0)
            ret=sum(self._created) / len(self._created), \
                   sum(self._deleted) / len(self._deleted), \
                   sum(self._moved) / len(self._moved), \
                   sum(self._modified) / len(self._modified), \
                   self._nfCreated, \
                   self._nfDeleted, \
                   self._nfMoved, \
                   self._nfModified
            self._nfCreated = self._nfDeleted = self._nfModified = self._nfMoved = 0
            return ret
        
g_w, g_top_level, g_root = None, None, None
monitoredDirectory = None
sendToAddress = None
g_observer = None
g_dirStatistics = dirStatistics(history_periods=100)
g_sendSocket = None

def getNumberOfFiles(dir):
    """count the number of files in given dir"""
    allfiles = []
    for _, __, files in os.walk(dir):
        allfiles.append(files)
        if len(allfiles) % 100 == 0:
            g_w.NumberOfFilesLabel['text'] = str(len(allfiles))
            g_w.NumberOfFilesLabel.update()
    g_w.NumberOfFilesLabel['text'] = str(len(allfiles))
    return len(allfiles)

def set_Tk_var():
    global monitoredDirectory
    monitoredDirectory = tk.StringVar()
    global sendToAddress
    sendToAddress = tk.StringVar()

def hostnameKeypress(p1):
    print('gui_support.hostnameKeypress')
    sys.stdout.flush()

def selectDirectory():
    global g_observer
    print('gui_support.selectDirectory')
    dir = tkinter.filedialog.askdirectory()
    monitoredDirectory.set(dir)
    nfFiles = getNumberOfFiles(dir)
    g_w.NumberOfFilesLabel['text'] = str(nfFiles)
    if g_observer:
        g_observer.stop()
        g_observer.join()
        g_observer = None
    g_dirStatistics.reset()
    g_observer = watchdog.observers.Observer()
    g_observer.schedule(g_dirStatistics, monitoredDirectory.get(), recursive=True) 
    g_observer.start()
    sys.stdout.flush()

def secondsTick(root):
    if monitoredDirectory.get():
        stats = g_dirStatistics.doStats()
        g_w.PercentageChangedLabel['text'] = "created=%2.2f, deleted=%2.2f, moved=%2.2f, modified=%2.2f" %stats[0:4]
        g_w.LatestLabel['text'] = "created=%2.2f, deleted=%2.2f, moved=%2.2f, modified=%2.2f" %stats[0:4]
        msg = messages.interchangeMessage(hostname="test", \
                                          dir=monitoredDirectory.get(),\
                                          nfFiles=0,\
                                          nfCreated=stats[0],\
                                          nfDeleted=stats[1],\
                                          nfMoved=stats[2],\
                                          nfModified=stats[3])
        print(msg)
        try:
            g_sendSocket.sendto(pickle.dumps(msg), (sendToAddress.get(), 1234))
            g_w.MessageLabel['text'] = "Successfully sent message"
            g_w.MessageLabel['foreground'] ="#000000"
        except OSError:
            g_w.MessageLabel['text'] = "Error in address, cannot send to master."
            g_w.MessageLabel['foreground'] ="#ff0000"
    root.after(1000, secondsTick, root)

def init(top, gui, *args, **kwargs):
    global g_w, g_top_level, g_root, g_sendSocket
    g_w = gui
    g_top_level = top
    g_root = top
    g_sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    g_sendSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    g_sendSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    g_root.after(1000, secondsTick, g_root)
    
def destroy_window():
    # Function which closes the window.
    global g_top_level
    g_top_level.destroy()
    g_top_level = None

if __name__ == '__main__':
    import gui
    gui.vp_start_gui()



