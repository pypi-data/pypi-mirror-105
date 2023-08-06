from curses import wrapper


def ui(stdscr):
    stdscr.clear()

    stdscr.refresh()
    stdscr.getkey()


wrapper(ui)
