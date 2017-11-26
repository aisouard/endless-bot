import argparse


def parse_args(args):
    parser = argparse.ArgumentParser(prog="endless-bot", description="A bot endlessly playing Endless Lake.")
    parser.add_argument(
        "-l", "--login", type=str, help="Facebook username", required=False, default=None)
    parser.add_argument(
        "-p", "--password", type=str, help="Facebook password", required=False, default=None)
    parser.add_argument(
        "-i", "--image", type=str, help="image file to scan", required=False, default=None)
    parser.add_argument(
        "-c", "--capture", type=str, help="folder to save the images into", required=False, default=None)
    parser.add_argument(
        "-b", "--blackbox", type=str, help="path to the blackbox file to write", required=False, default=None)
    parser.add_argument(
        "-d", "--disable-brain", help="disable all AI mechanics", action="store_true")
    parser.add_argument(
        "-s", "--supervised", type=str, help="path to the csv file to store supervised data", required=False, default=None)
    parser.add_argument(
        "-t", "--train", type=str, help="path to the csv file containing supervised data", required=False, default=None)
    return parser.parse_args(args)
