from tkinter import *

def pop_paramaters(root):

    def cancel():
        theme_choice.set(0)
        win.destroy()

    win = Toplevel(root)
    win.title("Параметры")
    win.resizable(False, False)

    win.protocol("WM_DELETE_WINDOW", cancel)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 300
    height = 120
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    win.geometry(F"{width}x{height}+{int(x)}+{int(y)}")

    Button(win, text="Применить", command=win.destroy).place(x=160, y=90)
    Button(win, text="Отмена", command=cancel).place(x=240, y=90)

    theme_choice = IntVar()

    Label(win, text="Выберите цветовую тему блокнота:").place(x=10, y=10)
    Radiobutton(win, text="Светлая", variable=theme_choice, value=1).place(x=10, y=30)
    Radiobutton(win, text="Тёмная", variable=theme_choice, value=2).place(x=10, y=50)

    win.grab_set()
    icon = PhotoImage(file=r"icons/adjust.png")
    win.iconphoto(False, icon)
    win.focus()

    win.wait_window()
    return theme_choice.get()