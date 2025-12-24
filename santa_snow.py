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
    """
    Draw string s at (y, x) but clip it to screen width/height.
    Prevents curses ERR by never drawing outside.
    """
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
        # Just in case terminal still complains
        pass


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    # Colors (if supported)
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

    snow = []  # list of dicts: {"x": int, "y": int, "ch": str, "speed": int}

    # Santa position: start off-screen right, move left
    h, w = stdscr.getmaxyx()
    santa_h = len(SANTA)
    santa_w = max(len(line) for line in SANTA)
    santa_y = max(0, (h // 2) - (santa_h // 2))
    santa_x = w  # start off-screen right
    santa_speed = 1

    last_time = time.time()

    while True:
        # Handle resize
        new_h, new_w = stdscr.getmaxyx()
        if (new_h, new_w) != (h, w):
            h, w = new_h, new_w
            santa_y = max(0, (h // 2) - (santa_h // 2))
            # keep santa_x as-is so motion feels continuous

        # Non-blocking key read (optional: press q to quit)
        ch = stdscr.getch()
        if ch in (ord("q"), ord("Q")):
            break

        # Spawn snow
        # More snow when screen is wider
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

        # Update positions
        for f in snow:
            f["y"] += f["speed"]

        # Remove off-screen snow
        snow = [f for f in snow if f["y"] < h]

        # Move santa right -> left
        santa_x -= santa_speed
        if santa_x < -santa_w:
            santa_x = w  # restart from right

        # Draw frame
        stdscr.erase()

        # Draw snow first (background)
        for f in snow:
            # Draw only if inside
            if 0 <= f["y"] < h and 0 <= f["x"] < w:
                try:
                    stdscr.addstr(f["y"], f["x"], f["ch"], SNOW_ATTR)
                except curses.error:
                    pass

        # Draw santa (foreground)
        for i, line in enumerate(SANTA):
            safe_addstr(stdscr, santa_y + i, santa_x, line, SANTA_ATTR)

        stdscr.refresh()

        # Frame cap
        now = time.time()
        dt = now - last_time
        last_time = now

        time.sleep(0.08)  # animation speed (slower/faster here)


if __name__ == "__main__":
    curses.wrapper(main)
