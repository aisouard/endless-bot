# -*- coding: utf-8 -*-

from importlib import reload
import numpy as np
import pygame
import unittest
from unittest.mock import Mock
from unittest.mock import patch

import endless_bot.receivers.pygamerenderer
from endless_bot.receivers.pygamerenderer import PygameRenderer


class PygameRendererTest(unittest.TestCase):
    def setUp(self):
        from endless_bot.main import parse_args
        self.args = parse_args([])
        self.random_image_a = np.random.randint(0, 255, (640, 360, 4), np.uint8)
        self.random_image_b = np.random.randint(0, 255, (640, 360, 4), np.uint8)

        self.GL = patch('OpenGL.GL').start()
        patch('pygame.font').start()
        self.pygame_display = patch('pygame.display').start()
        self.pygame_event = patch('pygame.event').start()
        self.pygame_init = patch('pygame.init').start()
        self.pygame_quit = patch('pygame.quit').start()

        reload(endless_bot.receivers.pygamerenderer)
        self.receiver = PygameRenderer(self.args)

    def tearDown(self):
        patch.stopall()

    def test_init(self):
        self.assertEqual(self.pygame_init.call_count, 1)
        self.assertEqual(self.pygame_display.set_mode.call_count, 1)

    def test_process_messages_idle(self):
        self.pygame_event.get.return_value = []
        result = self.receiver.process_messages({"original_image": self.random_image_a})
        self.assertEqual(result, 0)

        func, args, kwargs = self.GL.glTexImage2D.mock_calls[0]
        np.testing.assert_array_equal(args[8], self.random_image_a)

    def test_process_messages_modified_image(self):
        self.pygame_event.get.return_value = []
        result = self.receiver.process_messages({"original_image": self.random_image_a, "modified_image": self.random_image_b})
        self.assertEqual(result, 0)

        func, args, kwargs = self.GL.glTexImage2D.mock_calls[0]
        np.testing.assert_array_equal(args[8], self.random_image_b)

    def test_process_messages_escape(self):
        event = Mock()
        event.type = pygame.KEYUP
        event.key = pygame.K_ESCAPE
        self.pygame_event.get.return_value = [event]

        result = self.receiver.process_messages({"original_image": self.random_image_a})

        self.assertEqual(result, -1)
        self.assertEqual(self.pygame_quit.call_count, 1)

        func, args, kwargs = self.GL.glTexImage2D.mock_calls[0]
        np.testing.assert_array_equal(args[8], self.random_image_a)

    def test_process_messages_quit(self):
        event = Mock()
        event.type = pygame.QUIT
        pygame.event.get.return_value = [event]

        result = self.receiver.process_messages({"original_image": self.random_image_a})

        self.assertEqual(result, -1)
        self.assertEqual(self.pygame_quit.call_count, 1)

        func, args, kwargs = self.GL.glTexImage2D.mock_calls[0]
        np.testing.assert_array_equal(args[8], self.random_image_a)

    def test_process_messages_space(self):
        event = Mock()
        event.type = pygame.KEYUP
        event.key = pygame.K_SPACE
        pygame.event.get.return_value = [event]

        result = self.receiver.process_messages({"original_image": self.random_image_a})

        self.assertEqual(result, 1)

        func, args, kwargs = self.GL.glTexImage2D.mock_calls[0]
        np.testing.assert_array_equal(args[8], self.random_image_a)


if __name__ == '__main__':
    unittest.main()
