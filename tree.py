import curses
import random
import time
import math

WIDTH = 60
HEIGHT = 26

FLAKES = ['*', '.', '❄', '•']

TREE = [
    "          *",
    "         ***",
    "        *****",
    "       *******",
    "      *********",
    "     ***********",
    "    *************",
    "         |||",
    "         |||"
]

class Flake:
    __slots__ = ("x", "y", "vy", "phase", "char")

    def __init__(self, x):
        self.x = float(x)
        self.y = 0.0
        self.vy = random.choice([12.0, 14.0, 16.0])
        self.phase = random.uniform(0, math.tau)
        self.char = random.choice(FLAKES)

def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_GREEN, -1)
    curses.init_pair(5, curses.COLOR_CYAN, -1)

    tree_y = HEIGHT - len(TREE) - 2
    tree_x = (WIDTH // 2) - (len(TREE[-1]) // 2)

    flakes = []
    wind = 0.0
    target_wind = 0.0

    message = "Merry Christmas"
    msg_y = HEIGHT - 1

    last_t = time.time()

    while True:
        now = time.time()
        dt = clamp(now - last_t, 0.001, 0.05)
        last_t = now

        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            break
        if key in (curses.KEY_LEFT, ord('a'), ord('A')):
            target_wind -= 0.3
        elif key in (curses.KEY_RIGHT, ord('d'), ord('D')):
            target_wind += 0.3

        target_wind = clamp(target_wind, -3.0, 3.0)
        wind += (target_wind - wind) * 0.15

        if random.random() < 0.55:
            flakes.append(Flake(random.randint(0, WIDTH - 1)))

        new_flakes = []
        for f in flakes:
            f.phase += dt * random.uniform(2.5, 4.0)
            wobble = math.sin(f.phase) * 0.35

            f.y += f.vy * dt
            f.x += (wind * 2.0 * dt) + wobble

            if f.x < 0:
                f.x += WIDTH
            elif f.x >= WIDTH:
                f.x -= WIDTH

            if f.y < HEIGHT:
                new_flakes.append(f)

        flakes = new_flakes

        stdscr.erase()

        # draw snow
        for f in flakes:
            ix, iy = int(f.x), int(f.y)
            if 0 <= ix < WIDTH and 0 <= iy < HEIGHT:
                stdscr.addstr(iy, ix, f.char, curses.color_pair(5))

        # draw tree
        star_blink = int(now * 8) % 3
        star_color = [2, 3, 4][star_blink]

        for i, line in enumerate(TREE):
            for j, ch in enumerate(line):
                if ch == " ":
                    continue
                y = tree_y + i
                x = tree_x + j
                if i == 0 and ch == "*":
                    stdscr.addstr(y, x, "★", curses.color_pair(star_color) | curses.A_BOLD)
                elif ch == "*" and random.random() < 0.15:
                    stdscr.addstr(y, x, "●", curses.color_pair(random.choice([2,3,4])) | curses.A_BOLD)
                else:
                    stdscr.addstr(y, x, ch, curses.color_pair(1))

        # sparkling message
        msg_x = (WIDTH - len(message)) // 2
        for i, ch in enumerate(message):
            if random.random() < 0.12:
                color = random.choice([2,3,4])
                stdscr.addstr(msg_y, msg_x + i, ch, curses.color_pair(color) | curses.A_BOLD)
            else:
                stdscr.addstr(msg_y, msg_x + i, ch, curses.color_pair(1))

        stdscr.addstr(0, 0, f"Wind: {target_wind:+.1f}  (←/→ or A/D)  Quit: Q", curses.color_pair(5))

        stdscr.refresh()
        time.sleep(0.03)

if __name__ == "__main__":
    curses.wrapper(main)
