import curses
import random
import time

SANTA = [
    "　 ∩　∩　    ／￣`＞Ｏ",
    "　 い_cノ　(ニニニ)",
    "　c/･･ っ　(>∀<* )",
    "　(\"●\" )___とと　)",
    "　 ヽ　 ⌒､ |二二二|",
    "　　しし-し　┻━┻",
]

SNOW_CHARS = ["*", ".", "❄", "•",'❄️']


def safe_addstr(stdscr, y, x, s, attr=0):
 
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h:
        return

    # Entire string is left of screen or right of screen
    if x >= w or x + len(s) <= 0:
        return

    start = 0
    if x < 0:
        start = -x
        x = 0

    s = s[start:]
    if x + len(s) > w:
        s = s[: max(0, w - x)]

    if not s:
        return

    try:
        stdscr.addstr(y, x, s, attr)
    except curses.error:
        pass


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    # Colors 
    has_color = curses.has_colors()
    if has_color:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, -1)  # snow
        curses.init_pair(2, curses.COLOR_WHITE, -1)  # santa

        SNOW_ATTR = curses.color_pair(1)
        SANTA_ATTR = curses.color_pair(2)
    else:
        SNOW_ATTR = 0
        SANTA_ATTR = 0

    snow = [] 

    #산타 위치
    h, w = stdscr.getmaxyx()
    santa_h = len(SANTA)
    santa_w = max(len(line) for line in SANTA)
    santa_y = max(0, (h // 2) - (santa_h // 2))
    santa_x = w  # start off-screen right
    santa_speed = 1

    last_time = time.time()

    while True:
        new_h, new_w = stdscr.getmaxyx()
        if (new_h, new_w) != (h, w):
            h, w = new_h, new_w
            santa_y = max(0, (h // 2) - (santa_h // 2))

        ch = stdscr.getch()
        if ch in (ord("q"), ord("Q")):
            break

        spawn_prob = 0.25 if w < 80 else 0.35
        if random.random() < spawn_prob:
            snow.append(
                {
                    "x": random.randint(0, max(0, w - 1)),
                    "y": 0,
                    "ch": random.choice(SNOW_CHARS),
                    "speed": random.choice([1, 1, 2]),
                }
            )

        for f in snow:
            f["y"] += f["speed"]


        snow = [f for f in snow if f["y"] < h]


        santa_x -= santa_speed
        if santa_x < -santa_w:
            santa_x = w  

        # Draw frame
        stdscr.erase()


        for f in snow:
            if 0 <= f["y"] < h and 0 <= f["x"] < w:
                try:
                    stdscr.addstr(f["y"], f["x"], f["ch"], SNOW_ATTR)
                except curses.error:
                    pass

        for i, line in enumerate(SANTA):
            safe_addstr(stdscr, santa_y + i, santa_x, line, SANTA_ATTR)

        stdscr.refresh()


        now = time.time()
        dt = now - last_time
        last_time = now

        time.sleep(0.08) #스피드


if __name__ == "__main__":
    curses.wrapper(main)
