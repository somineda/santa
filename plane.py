
import curses
import random
import time
import locale

locale.setlocale(locale.LC_ALL, "")

# ======================
# ASCII ART (plane)
# ======================
PLANE = [
    ".　　　　　　　＿",
    "　　　⋀⋀　　 /　|",
    "　＿/(・ω・)／●. |",
    "!/　.}￣￣￣ 　　/",
    "i＼_}／￣|＿_／≡＝",
    "　　`￣￣~❤",
    " 　　　　　　～❤",
    " 　　　　　　　　～❤",
    " 　　　　　　　　　　～❤",
    " 　　　　　　　　　　　　～❤",
]

# 하트 떨어지는 시작점(비행기 기준 상대좌표)
# (대충 꼬리쪽 근처로)
HEART_SPAWN_REL_Y = 6   # 0부터 시작, 6번째 줄 근처
HEART_SPAWN_REL_X = 12  # 적당히 꼬리 근처



# ======================
# Safe draw helpers
# ======================
def safe_addstr(stdscr, y, x, s, attr=0):
    """화면 밖/유니코드로 curses ERR 나도 그냥 무시."""
    try:
        h, w = stdscr.getmaxyx()
        if y < 0 or y >= h or x >= w:
            return
        if x < 0:
            s = s[-x:]
            x = 0
        if x >= w:
            return
        s = s[: max(0, w - x)]
        if s:
            stdscr.addstr(y, x, s, attr)
    except curses.error:
        pass

# ======================
# Main
# ======================
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    curses.start_color()
    curses.use_default_colors()

    # color pairs
    # 1: white, 2: red, 3: cyan-ish, 4: yellow-ish (optional)
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_CYAN, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)

    WHITE = curses.color_pair(1)
    RED = curses.color_pair(2) | curses.A_BOLD

    # state
    plane_x = 0
    plane_y = 2

    hearts = []  # {"x": int, "y": int, "vy": int}
    snow = []    # {"x": int, "y": int, "vy": int, "ch": str}

    heart_tick = 0

    # 속도 (원하면 여기만 조절)
    FPS_DELAY = 0.06
    PLANE_SPEED = 1
    HEART_SPAWN_EVERY = 6      # 프레임마다 하트 생성 빈도(작을수록 더 많이)
    HEART_FALL_SPEEDS = [1, 1, 2]
    SNOW_SPAWN_RATE = 0.35     # 0~1 (클수록 눈 많이)
    SNOW_SPEEDS = [1, 1, 2]

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        # quit
        ch = stdscr.getch()
        if ch in (ord("q"), ord("Q")):
            break

        # center plane vertically a bit (if terminal small, keep safe)
        plane_h = len(PLANE)
        plane_w = max(len(line) for line in PLANE)
        if plane_y + plane_h >= h:
            plane_y = max(0, h - plane_h - 1)


        for f in list(snow):
            f["y"] += f["vy"]
            if f["y"] >= h - 1:
                snow.remove(f)


        # 시작은 화면 오른쪽 밖에서 시작
        if plane_x == 0:
            plane_x = w + 2

        plane_x -= PLANE_SPEED

        # 화면 왼쪽 완전 탈출하면 다시 오른쪽으로 리셋
        if plane_x < -plane_w - 2:
            plane_x = w + 2

        # ---- Heart spawn/update ----
        heart_tick += 1
        if heart_tick % HEART_SPAWN_EVERY == 0:
            hearts.append({
                "x": plane_x + HEART_SPAWN_REL_X,
                "y": plane_y + HEART_SPAWN_REL_Y,
                "vy": random.choice(HEART_FALL_SPEEDS),
            })

        for p in list(hearts):
            p["y"] += p["vy"]
            if p["y"] >= h - 1:
                hearts.remove(p)

        # ---- Draw snow ----
        for f in snow:
            safe_addstr(stdscr, f["y"], f["x"], f["ch"], WHITE)

        # ---- Draw plane (white) ----
        for i, line in enumerate(PLANE):
            safe_addstr(stdscr, plane_y + i, plane_x, line, WHITE)

        # ---- Draw falling hearts (red) ----
        # 하트 모양: ❤
        for p in hearts:
            safe_addstr(stdscr, p["y"], p["x"], "❤", RED)

        # hint
        safe_addstr(stdscr, 0, 2, "Press Q to quit", curses.A_DIM)

        stdscr.refresh()
        time.sleep(FPS_DELAY)

if __name__ == "__main__":
    curses.wrapper(main)
