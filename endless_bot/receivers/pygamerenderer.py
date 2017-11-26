# -*- coding: utf-8 -*-

import numpy as np
import os
import pygame
from OpenGL import GL

from endless_bot.receivers.abstractreceiver import AbstractReceiver

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VIEWPORT_SIZE = (360, 640)


class PygameRenderer(AbstractReceiver):
    def __init__(self, args):
        os.environ["SDL_VIDEO_CENTERED"] = "1"

        pygame.init()

        self._font = pygame.font.Font(os.path.join(ROOT_DIR, "..", "..", "assets", "VeraMono.ttf"), 14)
        self._font.set_bold(True)

        self._running = True
        self._screen = pygame.display.set_mode(VIEWPORT_SIZE, pygame.OPENGL | pygame.DOUBLEBUF)
        self._clock = pygame.time.Clock()
        self._image = GL.glGenTextures(1)

        GL.glClearDepth(1.)
        GL.glClearColor(0., 0., 0., 1.)
        GL.glViewport(0, 0, VIEWPORT_SIZE[0], VIEWPORT_SIZE[1])

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, VIEWPORT_SIZE[0], VIEWPORT_SIZE[1], 0, -1, 1)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glDisable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_TEXTURE_2D)

    def process_messages(self, messages):
        if not self._running:
            return -1

        image = messages["original_image"]
        if "modified_image" in messages:
            image = messages["modified_image"]

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glBindTexture(GL.GL_TEXTURE_2D, self._image)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB8, VIEWPORT_SIZE[0], VIEWPORT_SIZE[1], 0, GL.GL_BGR, GL.GL_UNSIGNED_BYTE, image)

        GL.glBegin(GL.GL_QUADS)
        GL.glTexCoord2f(0., 0.)
        GL.glVertex2f(0., 0.)
        GL.glTexCoord2f(1., 0.)
        GL.glVertex2f(VIEWPORT_SIZE[0], 0.)
        GL.glTexCoord2f(1., 1.)
        GL.glVertex2f(VIEWPORT_SIZE[0], VIEWPORT_SIZE[1])
        GL.glTexCoord2f(0., 1.)
        GL.glVertex2f(0., VIEWPORT_SIZE[1])
        GL.glEnd()

        pygame.display.set_caption("Endless Bot (FPS: %i)" % self._clock.get_fps())
        pygame.display.flip()
        self._clock.tick()
        action = self._handle_events()

        messages["action"] = action
        return action

    def text_to_image(self, text):
        surface = self._font.render(text, True, (255, 255, 255, 255), (0, 0, 0, 255))
        w, h = surface.get_width(), surface.get_height()
        image = pygame.image.tostring(surface, "RGB", False)
        return w, h, image

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self._running = False
                return -1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    self._running = False
                    return -1
                if event.key == pygame.K_SPACE:
                    return 1
        return 0
