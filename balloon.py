# -- coding: utf-8 --
# Original code by wontoncc (https://gist.github.com/wontonc)

from win32api import *
from win32gui import *
import win32con
import sys
import os
import struct
import time

ICON_PATH = os.path.abspath(os.path.join(sys.path[0], "balloontip.ico"))

class WindowsBalloonTip(object):
    def __init__(self):
        self._register_win_class()
        self._create_win()
        self._load_icon()
        self._add_notification(0)

    def show(self, title, msg):
        self._update_notification(title, msg)

    def destroy(self):
        DestroyWindow(self.hwnd)

    def _register_win_class(self):
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
        }
        
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map  # could also specify a wndproc.

        self.classAtom = RegisterClass(wc)
        self.hinst = hinst

    def _create_win(self):
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,
                                 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                 0, 0, self.hinst, None)
        UpdateWindow(self.hwnd)

    def _load_icon(self):
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            self.hicon = LoadImage(self.hinst, ICON_PATH,
                              win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            self.hicon = LoadIcon(0, win32con.IDI_APPLICATION)

    def _add_notification(self, id):
        self.id = id
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, self.id, flags, win32con.WM_USER+20, self.hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)

    def _update_notification(self, title, msg):
        Shell_NotifyIcon(NIM_MODIFY,
                         (self.hwnd, self.id, NIF_INFO, win32con.WM_USER+20,
                          self.hicon, "Balloon  tooltip", title, 200, msg))

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)  # Terminate the app.


BALLON_WIN = None

def balloon_tip(title, msg):
    global BALLON_WIN
    if BALLON_WIN is None:
        BALLON_WIN = WindowsBalloonTip()
    
    BALLON_WIN.show(title, msg)
