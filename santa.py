import sys
import time
import random
import math

# ======================
# Screen config
# ======================
WIDTH = 60
HEIGHT = 28
FPS = 14   # 느린 느낌

# ======================
# ANSI helpers
# ======================
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

def color256(n):
    return f"\033[38;5;{n}m"

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def clear():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

# ======================
# Santa ASCII (UNCHANGED)
# ======================
SANTA = [
"⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⠤⠶⣶⣶⠋⠳⡄⠀⠀⠀",
"⠀⠀⠀⠀⠀⢀⡖⠉⠀⠀⡰⠻⡅⠙⠲⠞⠁⠀⠀⠀",
"⠀⠀⠀⠀⢀⡾⠖⠚⠉⠉⠛⠲⢷⡀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⣼⢀⣠⣤⡤⢤⣤⣤⣀⣷⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⡴⠻⣍⠳⠖⣃⣘⠓⠖⣩⡟⢦⠀⠀⠀⠀⠀",
"⠀⠀⢰⡇⠀⢨⠿⠺⣇⣸⠗⠿⡅⠀⠘⡇⠀⠀⠀⠀",
"⠀⠀⠈⣧⠀⠛⠶⠚⠧⠼⠓⠶⠛⠀⣸⠧⣄⠀⠀⠀",
"⠀⠀⣰⠋⠹⡄⠀⠀⠀⠀⠀⠀⢠⠯⣥⣶⡮⡷⣄⠀",
"⠀⣸⢡⠞⠀⠙⠲⠤⣤⣤⠤⠖⠋⠀⣏⣀⣗⡷⠸⡆",
"⣰⢓⡟⠒⠶⠤⠤⢴⣻⣟⣶⠤⠤⢶⡏⠉⢻⠀⠀⢷",
"⢹⢻⣓⠲⠤⠤⠤⣼⡻⣟⣿⠤⠤⠬⠟⣛⡏⠀⠀⡾",
"⠈⢻⣌⠉⠓⠒⠶⠤⠭⠭⠥⠶⠒⠚⠉⣁⡟⠀⡴⠃",
"⠀⠀⠈⠻⣟⠒⠒⠦⣤⣤⠶⠖⠒⣻⣿⠥⠖⠋⠀⠀",
"⠀⠀⠀⠀⢨⣏⣉⣉⡇⢸⣉⣉⣹⡇⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⣇⣀⣀⣀⡇⢸⣀⣀⣀⣸⠀⠀"
]

# ======================
# Rainbow palette (smooth)
# ======================
RAINBOW = [
    196, 202, 208, 214, 220, 226,   # red → yellow
    190, 154, 118, 82, 46,          # green
    51, 45, 39, 33, 27, 21,         # blue
    57, 93, 129, 165                # purple
]

# ======================
# Snow
# ======================
SNOW_CHARS = ['❄', '•', '.', '·','❄️']
snow = []

def add_snow():
    if random.random() < 0.55:
        snow.append({
            "x": random.randint(0, WIDTH - 1),
            "y": 0,
            "speed": random.choice([1, 1, 2]),
            "char": random.choice(SNOW_CHARS),
        })

def update_snow():
    for f in list(snow):
        f["y"] += f["speed"]
        if f["y"] >= HEIGHT:
            snow.remove(f)

# ======================
# Draw functions
# ======================
def draw_santa(buf, frame):
    h = len(SANTA)
    w = max(len(l) for l in SANTA)
    start_y = 2
    start_x = (WIDTH - w) // 2

    # 산타 바디: 느린 무지개
    idx = (frame // 6) % len(RAINBOW)
    santa_color = color256(RAINBOW[idx])

    # 빨강 전구
    red_light = color256(196)

    for i, line in enumerate(SANTA):
        y = start_y + i
        if not (0 <= y < HEIGHT):
            continue

        is_hat_tip_line = ("⠋⠳⡄" in line) or ("⠲⠞⠁" in line)

        for j, ch in enumerate(line):
            x = start_x + j
            if not (0 <= x < WIDTH):
                continue
            if ch == "⠀":
                continue

            # 🎄 모자 끝: 전구로 변환 (랜덤)
            if is_hat_tip_line and random.random() < 0.15:
                buf[y][x] = red_light + BOLD + "●" + RESET
            else:
                buf[y][x] = santa_color + ch + RESET




def draw_message(buf, frame):
    msg = "Merry Christmas"
    y = HEIGHT - 3
    x = (WIDTH - len(msg)) // 2

    glow = (frame // 12) % 2 == 0
    color = color256(RAINBOW[(frame // 8) % len(RAINBOW)])
    style = BOLD if glow else DIM

    for i, ch in enumerate(msg):
        buf[y][x + i] = style + color + ch + RESET

def draw_snow(buf):
    for f in snow:
        if 0 <= f["y"] < HEIGHT:
            buf[f["y"]][f["x"]] = color256(255) + f["char"] + RESET

# ======================
# Main loop
# ======================
def main():
    hide_cursor()
    clear()

    frame = 0
    try:
        while True:
            buf = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

            draw_santa(buf, frame)
            draw_snow(buf)
            draw_message(buf, frame)

            sys.stdout.write("\033[H")
            sys.stdout.write("\n".join("".join(r) for r in buf))
            sys.stdout.flush()

            add_snow()
            update_snow()

            frame += 1
            time.sleep(1 / FPS)

    except KeyboardInterrupt:
        show_cursor()
        sys.stdout.write("\n🎄 Merry Christmas! 🎅\n")

if __name__ == "__main__":
    main()
