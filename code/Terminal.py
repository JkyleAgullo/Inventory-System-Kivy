import sys

def clear_screen():
    print("\033[H\033[J")

def design_box(x, y, max_width, max_length):
    for i in range(max_width):
        for j in range(max_length):
            if i == 0 or i == max_width - 1:
                if j == 0:
                    if i == 0:
                        gotoxy(x + j, y + i)
                        print(chr(201), end='')
                    elif i == max_width - 1:
                        gotoxy(x + j, y + i)
                        print(chr(200), end='')
                elif j == max_length - 1:
                    if i == 0:
                        gotoxy(x + j, y + i)
                        print(chr(187), end='')
                    elif i == max_width - 1:
                        gotoxy(x + j, y + i)
                        print(chr(188), end='')
                else:
                    gotoxy(x + j, y + i)
                    print(chr(205), end='')
            else:
                if j == 0 or j == max_length - 1:
                    gotoxy(x + j, y + i)
                    print(chr(179), end='')

def gotoxy(x, y):
    sys.stdout.write("\033[%d;%df" % (y, x))
    sys.stdout.flush()