import curses
import time
import random

SANTA = [
"┈░﻿ ░░░░░░ ░░░░░┈┈┈░",
"┈░░▄▇█████████▇▄-░░",
"┈▄█▉▀░╭▀▀▀▀▀▀▀▀▀╮░❤░▒",
"╭▀╮░░░╰┬─▄───▄─┬╯❤░",
"╰─╯░░░▄┴┐╭─└┘─╮├┐░░❤▒",
"┈┈▒▒▄█▌░└┘╰──╯└┘▐▄░",
"┈▒▒▒█▉▉▄░░░░░░░░░█▉",
]

BLINK_PATTERNS = ["╭▀╮", "╰─╯"]

FPS = 30
HEART_SPEED = 1

SNOW_CHARS = ["❄", "•", ".", "*",'❄️']
snow = []

def find_pattern_positions(lines, patterns):
    pos = set()
    for y, line in enumerate(lines):
        for pat in patterns:
            start = 0
            while True:
                idx = line.find(pat, start)
                if idx == -1:
                    break
                for j in range(len(pat)):
                    pos.add((y, idx + j))
                start = idx + len(pat)
    return pos

def find_heart_positions(lines):
    hearts = []
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == "❤":
                hearts.append((y, x))
    return hearts

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_MAGENTA, -1)

    WHITE = curses.color_pair(1)
    RED = curses.color_pair(2)
    HEARTS = [curses.color_pair(3), curses.color_pair(4)]

    blink_pos = find_pattern_positions(SANTA, BLINK_PATTERNS)
    heart_orig = find_heart_positions(SANTA)

    heart_particles = []
    for oy, ox in heart_orig:
        heart_particles.append({
            "ox": ox,
            "oy": oy,
            "offset": random.randint(0, 20)
        })

    t = 0
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        art_h = len(SANTA)
        art_w = max(len(line) for line in SANTA)
        top = max(0, (h - art_h) // 2)
        left = max(0, (w - art_w) // 2)

        # ❄ 눈 생성
        if random.random() < 0.5:
            snow.append({
                "x": random.randint(0, w - 1),
                "y": 0,
                "ch": random.choice(SNOW_CHARS),
                "speed": random.choice([1, 1, 2])
            })

        # ❄ 눈 이동
        for f in list(snow):
            f["y"] += f["speed"]
            if f["y"] >= h:
                snow.remove(f)

        # ❄ 눈 그리기
        for f in snow:
            if 0 <= f["y"] < h:
                safe_addstr(stdscr, f["y"], f["x"], f["ch"], WHITE)


        # 🎅 산타
        for y, line in enumerate(SANTA):
            for x, ch in enumerate(line):
                if ch == " " or ch == "❤":
                    continue

                dy = top + y
                dx = left + x
                if not (0 <= dy < h and 0 <= dx < w):
                    continue

                if (y, x) in blink_pos and random.random() < 0.15:
                    stdscr.addstr(dy, dx, ch, RED | curses.A_BOLD)
                else:
                    stdscr.addstr(dy, dx, ch, WHITE | curses.A_BOLD)


        for p in heart_particles:
            ox, oy, off = p["ox"], p["oy"], p["offset"]
            travel = (t * HEART_SPEED + off) % (oy + 6)
            yy = oy - travel
            if yy < 0:
                yy = oy

            dy = top + yy
            dx = left + ox
            if 0 <= dy < h and 0 <= dx < w:
                stdscr.addstr(
                    dy,
                    dx,
                    "❤",
                    random.choice(HEARTS) | curses.A_BOLD
                )

        msg = "Merry Christmas 15기 여러분!!"
        if h - 2 >= 0:
            stdscr.addstr(h - 2, max(0, (w - len(msg)) // 2), msg, WHITE)

        stdscr.refresh()

        if stdscr.getch() in (ord("q"), ord("Q")):
            break

        t += 1
        time.sleep(1 / FPS)
def safe_addstr(stdscr, y, x, ch, attr=0):
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h:
        return
    if x < 0 or x >= w:
        return
    try:
        stdscr.addstr(y, x, ch, attr)
    except curses.error:
        pass

if __name__ == "__main__":
    curses.wrapper(main)
