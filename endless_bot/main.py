# -*- coding: utf-8 -*-
import sys

from endless_bot.broadcaster import Broadcaster
from endless_bot.utils.parse_args import parse_args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    Broadcaster(args)
