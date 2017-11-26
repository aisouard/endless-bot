# -*- coding: utf-8 -*-

import cv2
from endless_bot.emitters.webbrowser import WebBrowser
from endless_bot.receivers.pygamerenderer import PygameRenderer


class Broadcaster:
    def __init__(self, args):
        self._receivers = []
        self._receivers.append(PygameRenderer(args))

        self._emitters = []

        if args.image:
            return

        self._emitters.append(WebBrowser(args, self))

    def send_image(self, image):
        action = 0
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        messages = {"original_image": image}

        for receiver in self._receivers:
            action = receiver.process_messages(messages)
            if action == -1:
                return -1

        return action
