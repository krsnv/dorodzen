#!/usr/bin/env python

""" Dorodzen

Pomodoro Timer running with Dzen2. Best timer for tiling window managers.
Forked from and inspired by Pododzen: https://github.com/wrl/pomodzen


@TODO: Create rc-file on first start
@TODO: Use rc-file for configuration
@TODO: Color themes support
@TODO: Instances offset while multiply timers running


BAR_WIDTH = 40
BAR_HEIGHT = 265

COLOR_BG = "#000"
COLOR_FG = "#5179A9"

FONT = "Terminus (TTF)"
FONT_SIZE = 9

DEFAULT_POMODORO_LENGHT = 25

"""

__version__ = "1.0"

import argparse
import time

from subprocess import Popen
from subprocess import PIPE
from subprocess import call

""" Default configuration """

bg = "#000"                # Background
fg = "#5179A9"             # Foreground
font = "Terminus (TTF)-9"  # Font (for timer digits)

width = 265  # Progress bar width
height = 40  # Prgoress bar height

pomodoro_length = (60) * 25  # Pomodoro lenght, in seconds
done_cmd = ""                # Default action after timer ends
max_offset = 220

dzen_cmd = [
    "dzen2",
    "-p",
    "-xs", "2",
    "-fn", font,
    "-bg", bg,
    "-fg", fg,
    "-ta", "l",
    "-h", 10,
    "-w", 200,
    "-y", "4",
    "-x", "300"]

dzen_ctrl = """^p({offset}){m:02.0f}:{s:02.0f}^p(+5)^r(500x40)
"""


class dzen(object):
    pipe_to = None

    def __init__(self, cmd):
        self.pipe_to = Popen([str(x) for x in cmd], stdin=PIPE)

    def kill(self):
        self.pipe_to.kill()


class dorodzen(dzen):
    start = None
    now = None
    end = None

    last_left = None
    last_offset = None

    def __init__(self, length, cmd, done_cmd):
        dzen.__init__(self, cmd)

        self.start = time.time()
        self.now = self.start
        self.end = self.start + length + 1

        self.done_cmd = done_cmd

    def __call__(self):
        while True:
            self.now = time.time()
            if self.now > self.end:
                break

            self.update(dzen_ctrl)
            time.sleep(.1)

        call(self.done_cmd, shell=True)
        self.kill()

    def update(self, ctrl):
        left = self.end - self.now
        offset = int(max_offset - ((left / pomodoro_length) * max_offset))

        if left == self.last_left and offset == self.last_offset:
            return

        self.last_left = left
        self.last_offset = offset

        m = left // 60
        s = int(left - (m * 60))

        ctrl = ctrl.format(m=m, s=s, h=height, offset=offset)

        self.pipe_to.stdin.write(ctrl.encode("ascii"))


def main():
    global pomodoro_length, done_cmd

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l",
        "--length",
        dest="length",
        help="Length. seconds unless given in the form of '25m'")

    parser.add_argument(
        "-c",
        "--command",
        dest="done_cmd",
        help="Command to run at the end of a timer")

    args = parser.parse_args()

    if args.length:
        length = args.length

        if length[-1] == "m":
            length = float(length[:-1]) * 60
        elif length[-1] == "h":
            length = float(length[:-1]) * 60 * 60
        elif length[-1] == "s":
            length = float(length[:-1])
        else:
            length = float(length)

        pomodoro_length = length

    if args.done_cmd:
        done_cmd = args.done_cmd

    dorodzen(
        length=pomodoro_length,
        cmd=dzen_cmd,
        done_cmd=done_cmd)()


if __name__ == "__main__":
    main()
