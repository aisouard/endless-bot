# -*- coding: utf-8 -*-

from cefpython3 import cefpython as cef
from importlib import reload
import numpy as np
import os
import tempfile
import unittest
from unittest.mock import Mock, patch, mock_open

import endless_bot.emitters.webbrowser
from endless_bot.emitters.webbrowser import BrowserHandler
from endless_bot.emitters.webbrowser import WebBrowser


class WebBrowserTest(unittest.TestCase):
    def setUp(self):
        from endless_bot.main import parse_args
        self.args = parse_args([])

        self.broadcaster = Mock()
        self.webbrowser = Mock()
        self.random_image = np.random.randint(0, 255, (640, 360, 4), np.uint8)
        self.paint_buffer = Mock()
        self.paint_buffer.GetString.return_value = self.random_image.tostring()

    @patch("builtins.open", new_callable=mock_open(read_data="data"))
    def test_handler_init_preload(self, mock_file):
        reload(endless_bot.emitters.webbrowser)
        BrowserHandler(self.webbrowser, self.broadcaster)
        self.assertEqual(mock_file.call_count, 1)

    @patch("builtins.open", mock_open(read_data="data"))
    def test_handler_loading_state_pending(self):
        reload(endless_bot.emitters.webbrowser)
        browser_handler = BrowserHandler(self.webbrowser, self.broadcaster)
        browser_handler.OnLoadingStateChange(self.webbrowser, True)

        self.assertEqual(self.webbrowser.ExecuteJavascript.call_count, 0)

    @patch("builtins.open", mock_open(read_data="data"))
    def test_handler_loading_state_ready(self):
        reload(endless_bot.emitters.webbrowser)
        browser_handler = BrowserHandler(self.webbrowser, self.broadcaster)
        browser_handler.OnLoadingStateChange(self.webbrowser, False)

        self.assertEqual(self.webbrowser.ExecuteJavascript.call_count, 1)
        self.assertEqual(self.webbrowser.ExecuteJavascript.call_args, unittest.mock.call("data"))

    def test_handler_paint_invalid_element(self):
        reload(endless_bot.emitters.webbrowser)
        browser_handler = BrowserHandler(self.webbrowser, self.broadcaster)
        browser_handler.OnPaint(Mock(), cef.PET_POPUP, self.paint_buffer)

        self.assertEqual(self.paint_buffer.GetString.call_count, 0)
        self.assertEqual(self.broadcaster.send_image.call_count, 0)

    def test_handler_paint_continue(self):
        self.broadcaster.send_image.return_value = 0
        reload(endless_bot.emitters.webbrowser)
        browser_handler = BrowserHandler(self.webbrowser, self.broadcaster)
        browser_handler.OnPaint(Mock(), cef.PET_VIEW, self.paint_buffer)

        self.assertEqual(self.paint_buffer.GetString.call_count, 1)
        np.testing.assert_array_equal(self.broadcaster.send_image.call_args[0][0], self.random_image)

    def test_handler_paint_shutdown(self):
        self.broadcaster.send_image.return_value = -1
        reload(endless_bot.emitters.webbrowser)
        browser_handler = BrowserHandler(self.webbrowser, self.broadcaster)
        browser_handler.OnPaint(Mock(), cef.PET_VIEW, self.paint_buffer)

        self.assertEqual(self.paint_buffer.GetString.call_count, 1)
        np.testing.assert_array_equal(self.broadcaster.send_image.call_args[0][0], self.random_image)
        self.assertEqual(self.webbrowser.shutdown.call_count, 1)

    def test_handler_paint_click(self):
        action = np.random.randint(1, 600, 1)
        self.broadcaster.send_image.return_value = action
        reload(endless_bot.emitters.webbrowser)
        browser_handler = BrowserHandler(self.webbrowser, self.broadcaster)
        browser_handler.OnPaint(Mock(), cef.PET_VIEW, self.paint_buffer)

        self.assertEqual(self.webbrowser.send_click.call_count, 1)
        self.assertEqual(self.webbrowser.send_click.call_args, unittest.mock.call(180, action))

    def test_handler_get_view_rect(self):
        reload(endless_bot.emitters.webbrowser)
        browser_handler = BrowserHandler(self.webbrowser, self.broadcaster)

        rect_out = []
        result = browser_handler.GetViewRect(rect_out)

        self.assertEqual(rect_out, [0, 0, 360, 640])
        self.assertEqual(result, True)

    @patch('appdirs.user_data_dir')
    @patch('cefpython3.cefpython')
    def test_cache_dir(self, cef_mock, user_data_dir):
        parent_dir = tempfile.mkdtemp()
        cache_dir = os.path.join(parent_dir, "Browser")

        self.assertFalse(os.path.isdir(cache_dir))
        user_data_dir.return_value = parent_dir

        cef_mock.__version__ = "55.3"
        reload(endless_bot.emitters.webbrowser)
        WebBrowser(self.args, self.broadcaster)

        self.assertEqual(user_data_dir.call_count, 1)
        self.assertEqual(cef_mock.Initialize.call_args_list[0][0][0]["cache_path"], cache_dir)
        self.assertEqual(cef_mock.MessageLoop.call_count, 1)
        self.assertEqual(cef_mock.Shutdown.call_count, 1)
