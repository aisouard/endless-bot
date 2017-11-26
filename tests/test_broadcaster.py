# -*- coding: utf-8 -*-

import cv2
import numpy as np
from importlib import reload
import unittest
from unittest.mock import Mock
from unittest.mock import patch

import endless_bot.broadcaster


class BroadcasterTest(unittest.TestCase):
    def setUp(self):
        from endless_bot.utils.parse_args import parse_args
        self.empty_args = parse_args([])
        self.capture_args = parse_args(["-c", "captures"])
        self.image_args = parse_args(["-i", "image.png"])
        self.blackbox_args = parse_args(["-b", "blackbox.dat"])
        self.disable_brain_args = parse_args(["-d"])

        self.web_browser = patch('endless_bot.emitters.webbrowser.WebBrowser').start()
        self.pygame_renderer = patch('endless_bot.receivers.pygamerenderer.PygameRenderer').start()

        self.image = np.random.randint(0, 255, (640, 360, 4), np.uint8)
        self.image_without_alpha = cv2.cvtColor(self.image, cv2.COLOR_BGRA2BGR)

        reload(endless_bot.broadcaster)

    def tearDown(self):
        patch.stopall()

    def test_init_empty_args(self):
        from endless_bot.broadcaster import Broadcaster
        broadcaster = Broadcaster(self.empty_args)

        self.assertEqual(self.pygame_renderer.call_count, 1)
        self.assertEqual(self.pygame_renderer.call_args, unittest.mock.call(self.empty_args))

        self.assertEqual(self.web_browser.call_count, 1)
        self.assertEqual(self.web_browser.call_args, unittest.mock.call(self.empty_args, broadcaster))

    def test_init_capture_args(self):
        from endless_bot.broadcaster import Broadcaster
        broadcaster = Broadcaster(self.capture_args)

        self.assertEqual(self.pygame_renderer.call_count, 1)
        self.assertEqual(self.pygame_renderer.call_args, unittest.mock.call(self.capture_args))

        self.assertEqual(self.web_browser.call_count, 1)
        self.assertEqual(self.web_browser.call_args, unittest.mock.call(self.capture_args, broadcaster))

    def test_init_image_args(self):
        from endless_bot.broadcaster import Broadcaster
        broadcaster = Broadcaster(self.image_args)

        self.assertEqual(self.pygame_renderer.call_count, 1)
        self.assertEqual(self.pygame_renderer.call_args, unittest.mock.call(self.image_args))

        self.assertEqual(self.web_browser.call_count, 0)

    def test_init_disable_brain_args(self):
        from endless_bot.broadcaster import Broadcaster
        broadcaster = Broadcaster(self.disable_brain_args)

        self.assertEqual(self.pygame_renderer.call_count, 1)
        self.assertEqual(self.pygame_renderer.call_args, unittest.mock.call(self.disable_brain_args))

        self.assertEqual(self.web_browser.call_count, 1)
        self.assertEqual(self.web_browser.call_args, unittest.mock.call(self.disable_brain_args, broadcaster))

    def test_init_empty_args_send_image_call_receivers(self):
        pygame_renderer_handle = Mock()

        pygame_renderer_handle.return_value = 0

        self.pygame_renderer.return_value.process_messages = pygame_renderer_handle

        from endless_bot.broadcaster import Broadcaster
        broadcaster = Broadcaster(self.empty_args)
        broadcaster.send_image(self.image)

        pygame_renderer_image_arg = pygame_renderer_handle.call_args[0][0]

        np.testing.assert_array_equal(pygame_renderer_image_arg["original_image"], self.image_without_alpha)

    def test_init_capture_args_send_image_call_receivers(self):
        pygame_renderer_handle = Mock()

        pygame_renderer_handle.return_value = 0

        self.pygame_renderer.return_value.process_messages = pygame_renderer_handle

        from endless_bot.broadcaster import Broadcaster
        broadcaster = Broadcaster(self.capture_args)
        broadcaster.send_image(self.image)

        pygame_renderer_image_arg = pygame_renderer_handle.call_args[0][0]

        np.testing.assert_array_equal(pygame_renderer_image_arg["original_image"], self.image_without_alpha)

    def test_init_empty_args_send_image_return_value(self):
        from endless_bot.broadcaster import Broadcaster

        pygame_renderer_handle = Mock()

        self.pygame_renderer.return_value.process_messages = pygame_renderer_handle

        for i in range(-1, 1):
            pygame_renderer_handle.return_value = i

            broadcaster = Broadcaster(self.empty_args)
            result = broadcaster.send_image(self.image)

            self.assertEqual(result, i)


if __name__ == '__main__':
    unittest.main()
