# -*- coding: utf-8 -*-

from cefpython3 import cefpython as cef
import appdirs
import numpy as np
import os
import sys

from endless_bot.emitters.abstractemitter import AbstractEmitter

GAME_URL = "https://apps.facebook.com/611307059053310"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VIEWPORT_SIZE = (360, 640)


def _check_version():
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"


class BrowserHandler:
    def __init__(self, parent, broadcaster):
        self.parent = parent
        self.broadcaster = broadcaster

        with open(os.path.join(ROOT_DIR, "..", "..", "assets", "preload.js"), "r") as f:
            self._preload = f.read()
            f.close()

    def OnLoadingStateChange(self, browser, is_loading, **_):
        if is_loading:
            return

        browser.ExecuteJavascript(self._preload)

    def OnPaint(self, browser, element_type, paint_buffer, **_):
        if element_type != cef.PET_VIEW:
            return

        buffer = paint_buffer.GetString(mode="bgra", origin="top-left")
        image = np.fromstring(buffer, dtype=np.uint8).reshape((VIEWPORT_SIZE[1], VIEWPORT_SIZE[0], 4))
        action = self.broadcaster.send_image(image)

        if action == -1:
            self.parent.shutdown()
            return

        if action == 0:
            return

        self.parent.send_click(VIEWPORT_SIZE[0] / 2, action)

    def GetViewRect(self, rect_out, **_):
        rect_out.extend([0, 0, VIEWPORT_SIZE[0], VIEWPORT_SIZE[1]])
        return True


class WebBrowser(AbstractEmitter):
    def __init__(self, args, broadcaster):
        self._cef_browser = None
        self._handler = BrowserHandler(self, broadcaster)
        self._credentials = [args.login, args.password]

        _check_version()
        self._setup_browser()

    def shutdown(self):
        if self._cef_browser:
            self._cef_browser.CloseBrowser(True)
            self._cef_browser = None
        cef.QuitMessageLoop()

    def send_click(self, x, y):
        browser = self._cef_browser
        browser.SendMouseMoveEvent(x, y, False, 0)
        browser.SendMouseClickEvent(x, y, cef.MOUSEBUTTON_LEFT, mouseUp=False, clickCount=1)
        browser.SendMouseClickEvent(x, y, cef.MOUSEBUTTON_LEFT, mouseUp=True, clickCount=1)

    def _setup_browser(self):
        init_settings = {
            "cache_path": os.path.join(appdirs.user_data_dir("EndlessLake", appauthor=False), "Browser"),
            "persist_session_cookies": True
        }

        switches = {
            "disable-d3d11": "",
            "enable-begin-frame-scheduling": "",
        }

        browser_settings = {
            "windowless_frame_rate": "30",
        }

        sys.excepthook = cef.ExceptHook
        cef.Initialize(init_settings, switches)

        window_info = cef.WindowInfo()
        parent_window_handle = 0
        window_info.SetAsOffscreen(parent_window_handle)

        self._cef_browser = cef.CreateBrowserSync(window_info, url=GAME_URL, settings=browser_settings)
        self._cef_browser.SetJavascriptBindings(self._init_bindings())
        self._cef_browser.SetClientHandler(self._handler)
        self._cef_browser.SendFocusEvent(True)
        self._cef_browser.WasResized()

        cef.MessageLoop()
        cef.Shutdown()

    def _get_credentials(self, callback):
        callback.Call(self._credentials)

    def _send_ready(self, callback):
        self._handler.ready = True
        callback.Call(0)

    def _init_bindings(self):
        bindings = cef.JavascriptBindings(bindToFrames=False, bindToPopups=False)
        bindings.SetFunction("__endless_bot__getCredentials", self._get_credentials)
        bindings.SetFunction("__endless_bot__sendReady", self._send_ready)
        return bindings
