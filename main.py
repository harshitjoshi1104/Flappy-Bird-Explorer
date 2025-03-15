'''
----------------------------------- Flappy bird on windows explorer -------------------------------------------------
'''

import time
import os
import win32com.client
import pyautogui, pythoncom
import threading
import random
import keyboard

# GLobals
MAX_COL_COUNT = 20   # 20 file per row
MAX_ROW_COUNT = 8
MAX_FILE_NUMBER = 160

DEFAULT_TIME_FRAME = 2
MIN_TIME_FOR_PIPES_TO_APPEAR_S = 15
LAST_TIME_US = 0
CURRENT_COL_BUCKET_TOP = {}
NEXT_BUCKET_TOP = {}
CURRENT_COL_BUCKET_BOTTOM = {}
NEXT_BUCKET_BOTTOM = {}

GAME_INIT_COMPLETE = 0

GAME_EXIT = 0

CURRENT_FLAPPY_BIRD_POS = MAX_FILE_NUMBER - MAX_COL_COUNT

# Getting directory
os.chdir("D:\Random Personal Code\Flappy Bird\Game")
current = os.getcwd()

# Icons
white_icon_path = "D:\\Random Personal Code\\Flappy Bird\\FB_files\\white_txt.ico"
green_icon_path = "D:\\Random Personal Code\\Flappy Bird\\FB_files\\green_txt.ico"
flappy_bird_path = "D:\\Random Personal Code\\Flappy Bird\\FB_files\\flappy_bird.ico"


# Starting creating game txt files (n*m)
def game_init():
    # Creating working directory
    pythoncom.CoInitialize()
    for i in range(160):
        text_file_path = f'{current}\\text_{i}.lnk'
        shell = win32com.client.Dispatch("WScript.shell")
        shortcut = shell.CreateShortcut(os.path.abspath(text_file_path))
        shortcut.IconLocation = os.path.abspath(white_icon_path)
        shortcut.Save()


def color_text_file(file_number, value):
    global current
    pythoncom.CoInitialize()
    text_file = f"{current}\\text_{file_number}.lnk"
    shell = win32com.client.Dispatch("WScript.shell")
    shortcut = shell.CreateShortcut(os.path.abspath(text_file))
    # if (file_number == CURRENT_FLAPPY_BIRD_POS) and GAME_INIT_COMPLETE == 1:
    #     return

    if value == "green":
        shortcut.IconLocation = os.path.abspath(green_icon_path)
    elif value == "white":
        shortcut.IconLocation = os.path.abspath(white_icon_path)
    else:
        shortcut.IconLocation = os.path.abspath(flappy_bird_path)
    shortcut.Save()


def set_pipe(column, isTop, length):
    if isTop:
        current_file = column
        while length > 0 and current_file < MAX_FILE_NUMBER:
            length-=1
            color_text_file(current_file, "green")
            current_file += MAX_COL_COUNT

    else:
        current_file = (MAX_FILE_NUMBER - MAX_COL_COUNT) + column
        while length > 0 and current_file > -1:
            length-=1
            color_text_file(current_file, "green")
            current_file -= MAX_COL_COUNT


def reset_pipe_column(column, isTop, length):
    if isTop:
        current_file = column
        while length > 0 and current_file < MAX_FILE_NUMBER:
            length-=1
            if current_file != CURRENT_FLAPPY_BIRD_POS:
                color_text_file(current_file, "white")

            current_file += MAX_COL_COUNT

def refresh_window():
    global REFRESH_WINDOW
    if REFRESH_WINDOW == 1:
        return
    REFRESH_WINDOW = 1
    while True:
        pyautogui.press('f5')
        time.sleep(0.3)


def swap_file(file1,file2, size, t_count, isFlappy=False):
    global GAME_EXIT
    if not isFlappy:
        if file2 == CURRENT_FLAPPY_BIRD_POS:
            GAME_EXIT = 1
            print("Game Exit!!")
            exit(1)

    if not isFlappy and file2 == -1:
        return
    complete_path = ''
    temp_file = complete_path + f"dummy_temp_{size}_{t_count}.lnk"
    current_file = complete_path + f"text_{file1}.lnk"
    final_file = complete_path + f"text_{file2}.lnk"

    os.rename(current_file, temp_file)
    os.rename(final_file, current_file)
    os.rename(temp_file, final_file)

def new_worker_job(item):
    global CURRENT_COL_BUCKET_TOP, CURRENT_COL_BUCKET_BOTTOM
    global NEXT_BUCKET_TOP, NEXT_BUCKET_BOTTOM
    if item%MAX_COL_COUNT == 0:
        reset_pipe_column(0, 1, MAX_ROW_COUNT)
        return

    current_top = item
    current_bottom = (MAX_FILE_NUMBER - MAX_COL_COUNT) + item
    curr_length_top = CURRENT_COL_BUCKET_TOP[item][0]
    curr_length_bottom = CURRENT_COL_BUCKET_TOP[item][1]

    if current_top%MAX_COL_COUNT - 1:
        set_pipe(item, 1, curr_length_top)

    if current_bottom%MAX_COL_COUNT == MAX_COL_COUNT - 1:
        set_pipe(item, 0, curr_length_bottom)
    while curr_length_top > 0:
        swap_file(current_top, current_top-1, curr_length_top, current_top%MAX_COL_COUNT)
        current_top += MAX_COL_COUNT
        curr_length_top-=1

    while curr_length_bottom > 0:
        swap_file(current_bottom, current_bottom-1, curr_length_bottom, current_bottom%MAX_COL_COUNT)
        current_bottom -= MAX_COL_COUNT
        curr_length_bottom-=1

    if item%MAX_COL_COUNT > 0:
        NEXT_BUCKET_TOP[item-1] = CURRENT_COL_BUCKET_TOP[item]
    # else:
        # reset_pipe_column(0, 1, MAX_ROW_COUNT)

def MovePipe():
    global CURRENT_COL_BUCKET_TOP, CURRENT_COL_BUCKET_BOTTOM
    global NEXT_BUCKET_TOP, NEXT_BUCKET_BOTTOM, GAME_EXIT
    while True:
        if GAME_EXIT == 1:
            break
        time.sleep(DEFAULT_TIME_FRAME)
        CURRENT_COL_BUCKET_TOP = {item:NEXT_BUCKET_TOP[item] for item in NEXT_BUCKET_TOP}
        NEXT_BUCKET_TOP = {}
        worker_thread = []
        for item in CURRENT_COL_BUCKET_TOP:
            worker_thread.append(threading.Thread(target=new_worker_job, args=(item,)))
            worker_thread[-1].start()

        for worker in worker_thread:
            worker.join()
        pyautogui.press('f5')

def Create_Pipes():
    top_pipe_length = random.randint(0, MAX_ROW_COUNT - 2)
    bottom_pip_length = random.randint(0, MAX_ROW_COUNT-top_pipe_length-2)

    if top_pipe_length:
        NEXT_BUCKET_TOP[MAX_COL_COUNT-1] = (top_pipe_length, bottom_pip_length)

    if bottom_pip_length:
        NEXT_BUCKET_BOTTOM[MAX_COL_COUNT-1] = bottom_pip_length


def move_flappy_bird(event):
    global CURRENT_FLAPPY_BIRD_POS, MAX_COL_COUNT, MAX_FILE_NUMBER

    if event.name == "W" or event.name == "w":
        # Check if already in top row
        if CURRENT_FLAPPY_BIRD_POS < 20:
            return
        new_pos = CURRENT_FLAPPY_BIRD_POS - MAX_COL_COUNT

    elif event.name == "S" or event.name == "s":
        if CURRENT_FLAPPY_BIRD_POS >= (MAX_FILE_NUMBER - MAX_COL_COUNT):
            return
        new_pos = CURRENT_FLAPPY_BIRD_POS + MAX_COL_COUNT

    elif event.name == "A" or event.name == "a":
        if CURRENT_FLAPPY_BIRD_POS%MAX_COL_COUNT == 0:
            return
        new_pos = CURRENT_FLAPPY_BIRD_POS - 1

    elif event.name == "D" or event.name == "d":
        if (CURRENT_FLAPPY_BIRD_POS + 1)%MAX_COL_COUNT == 0:
            return
        new_pos = CURRENT_FLAPPY_BIRD_POS + 1

    else:
        return
    swap_file(CURRENT_FLAPPY_BIRD_POS, new_pos, 100000, 1293240, isFlappy=True)
    CURRENT_FLAPPY_BIRD_POS = new_pos


def create_flappy_bird_instance():
    global CURRENT_FLAPPY_BIRD_POS
    global GAME_EXIT
    color_text_file(CURRENT_FLAPPY_BIRD_POS, "flappy")
    keyboard.on_press(move_flappy_bird)

    while GAME_EXIT == 0:
        time.sleep(2)

    keyboard.unhook_all()


def main():
    global GAME_INIT_COMPLETE
    game_init()
    for i in range(MAX_COL_COUNT):
        reset_pipe_column(i, 1, 6)
    time.sleep(5)

    t1 = threading.Thread(target=MovePipe)
    t1.start()
    t2 = threading.Thread(target=create_flappy_bird_instance)
    t2.start()
    GAME_INIT_COMPLETE = 1
    time.sleep(2)
    while True:
        if GAME_EXIT == 1:
            break
        Create_Pipes()
        time.sleep(MIN_TIME_FOR_PIPES_TO_APPEAR_S)


main()

