# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class AbstractReceiver(ABC):
    @abstractmethod
    def process_messages(self, messages):
        pass
