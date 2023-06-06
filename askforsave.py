from tkinter import Button, Toplevel, LabelFrame, Text, TRUE, BOTH, PhotoImage

def askforsave(win, file_name):
    root = Toplevel(win)

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    width = 355
    height = 128
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry(F"{width}x{height}+{int(x)}+{int(y)}")

    def save():
        root.value = True
        root.destroy()
    
    def dontsave():
        root.value = False
        root.destroy()
    
    def cancel():
        root.value = None
        root.destroy()

    root.title("Сохранение")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", cancel)

    top = LabelFrame(root, bg="white", bd=0, height=10)
    bot = LabelFrame(root, bg="#f0f0f0", bd=1, height=0, pady = 5)

    l1 = Text(top, bd=0, font="Lucida 11", padx=10, pady=10, spacing1=3, fg="#003399", cursor="")
    l1.insert(1.0, f'Вы хотите сохранить изменения в файле\n"{file_name}"?')
    l1.pack(expand=TRUE, fill=BOTH)
    l1.bindtags((str(l1), str(root), "all"))
    l1["height"] = 0
    
    bPos = Button(bot, text="Сохранить", font="Lucida 9", bd=1, bg="#e1e1e1", padx=16, activebackground="#cce4f7", command=save)
    bPos.place(x=35, y=5)
    bPos.bind("<Enter>", lambda e: bPos.config(background='#e5f1fb'))
    bPos.bind("<Leave>", lambda e: bPos.config(background='#e1e1e1'))

    bNeg = Button(bot, text="Не сохранять", font="Lucida 9", bd=1, bg="#e1e1e1", padx=16, activebackground="#cce4f7", command=dontsave)
    bNeg.place(x=140, y=5)
    bNeg.bind("<Enter>", lambda e: bNeg.config(background='#e5f1fb'))
    bNeg.bind("<Leave>", lambda e: bNeg.config(background='#e1e1e1'))

    bCancel = Button(bot, text="Отмена", font="Lucida 9", bd=1, bg="#e1e1e1", padx=16, activebackground="#cce4f7", command=cancel)
    bCancel.place(x=260, y=5)
    bCancel.bind("<Enter>", lambda e: bCancel.config(background='#e5f1fb'))
    bCancel.bind("<Leave>", lambda e: bCancel.config(background='#e1e1e1'))

    top.pack(expand=TRUE, fill=BOTH)
    bot.pack(expand=TRUE, fill=BOTH)

     
    root.grab_set()
    root.focus()
    root.wait_window()
    return root.value