from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from askforsave import askforsave
from encryption import encrypt
from parameters import pop_paramaters
from configparser import ConfigParser

INITIAL_WIDTH, INITIAL_HEIGHT = 550, 650 # Ширина и высота окна при запуске программы
DEFAULT_FONT_SIZE = 11 # Стандартный размер шрифта
current_font_size = DEFAULT_FONT_SIZE # Текущий размер шрифта

def save_file(e=None):
        global file_name
        global file_path
        global selected_text
        global is_saved
        global file_is_created
        global cancelling
        global save_dialog_closed
        global info_opened
        global previous_clipboard_state
        global initial_text
        if not is_saved:
            text = str(field.get("1.0", END))
            if not file_is_created:
                file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Текстовый файл", ".txt"), ("Все файлы", ".*")])
                if file is None:
                        save_dialog_closed = True
                        return
                with open(file.name, "w", encoding="utf-8") as f:
                    file_is_created = True
                    file_path = file.name
                    name = str((file.name.split("/"))[-1])
                    root.title(f"{name} - AmTCD")
                    file_name = str((file.name.split("/"))[-1])
                    f.write(encrypt(text, keyP, keyK))
                    initial_text = str(field.get("1.0", END))
            else:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(encrypt(text, keyP, keyK))
                initial_text = str(field.get("1.0", END))
                check_unsaved()
            is_saved = True
        if is_saved and not file_is_created:
            save_as()

def change_color_theme():
        choice = pop_paramaters(root)
        match choice:
            case 1:
                field.config(bg="white")
                field.config(fg="black")
                field.config(insertbackground="black")
            case 2:
                field.config(bg="#10100F")
                field.config(fg="#FAFADE")
                field.config(insertbackground="white")

def change_scale(event): # Изменение размера шрифта колесиком мыши
        global current_font_size
        if event.num == 5 or event.delta == -120: # Колесико вниз
            if current_font_size >= 1: current_font_size -= 2
        if event.num == 4 or event.delta == 120: # Колесико вверх     
            if current_font_size <= 1000: current_font_size += 2
        field.config(font=f"Consolas {current_font_size}")

def set_default_scale(e=None):
    global current_font_size
    field.config(font=f"Consolas {DEFAULT_FONT_SIZE}")
    current_font_size = DEFAULT_FONT_SIZE
                
def pop_about(): messagebox.showinfo("О программе", 'Программа для "прозрачного шифрования"\n© Rudenok M.I., Russia, 2023\n rudenok.2003@mail.ru')

def pop_info():
    def on_closing():
        global info_opened
        info_opened = False
        win.destroy()
        
    global info_opened
    if not info_opened:
        info_opened = True
        win = Toplevel(root)
        win.title("Справка")
        win.resizable(False, False)
        win.protocol("WM_DELETE_WINDOW", on_closing)
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        width = 366
        height = 195
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        win.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        text = Text(win, font=("Consolas", 11), padx=6, pady=6, bg="#f0f0f0", height=11, bd=0, cursor="")
        text.insert(1.0, 'Приложение с графическим интерфейсом\n"Блокнот TCD" (файл приложения: TCD).\nПозволяет: создавать / открывать / сохранять'
                    '\nзашифрованный текстовый файл, предусмотрены\nввод и сохранение личного ключа,\nвывод не модальной формы "Справка",'
                    '\nвывод модальной формы "О программе".')
        text.config(state=DISABLED)
        text.pack()
        close_button = Button(win, text="Закрыть", height=2, width=8, command=on_closing, bg="#b3b3b3", font=("TkDefaultFont", 11), bd=2)
        close_button.place(x=280, y=145)
        icon = PhotoImage(file=r"icons/question-sign.png")
        win.iconphoto(False, icon)
        win.focus()
        win.mainloop()

def save_as(e=None):
    global file_path
    global initial_text
    global is_saved
    global file_is_created
    text = str(field.get("1.0", END))
    file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Текстовый файл", ".txt"), ("Все файлы", ".*")])
    if file is None: return
    with open(file.name, "w", encoding="utf-8") as f:
        f.write(encrypt(text, keyP, keyK))
        file_path = file.name
        file_name = str((file.name.split("/"))[-1])
        root.title(f"{file_name} - AmTCD")
        initial_text = str(field.get("1.0", END))
        is_saved = True
        file_is_created = True
    
def new_file(e=None): # Создание нового файла
    global file_name
    global initial_text
    global file_path
    global file_is_created
    global is_saved
    global cancelling
    global save_dialog_closed
    if not is_saved: ask_for_save()
    if not cancelling and not save_dialog_closed:
        root.title("Безымянный - AmTCD")
        file_name = "Безымянный"
        field.delete(1.0, END)
        initial_text = str(field.get("1.0", END))
        file_path = None
        is_saved = True
        file_is_created = False
    cancelling = False
    save_dialog_closed = False

def check_unsaved(e=None):
    global is_saved
    current_text = str(field.get("1.0", END))
    if current_text != initial_text:
        is_saved = False
        root.title(f"*{file_name} - AmTCD")
    else:
        is_saved = True
        root.title(f"{file_name} - AmTCD")

def open_file(e=None): # Открытие существующего файла
    global is_saved
    global file_path
    global is_saved
    global cancelling
    global save_dialog_closed
    global initial_text
    global file_is_created
    if not is_saved: ask_for_save()
    if not cancelling and not save_dialog_closed:
        file = filedialog.askopenfilename()
        if len(file) == 0: return
        file_path = file
        with open(file, "r", encoding = "utf-8") as f:
            text = f.read()
            file_name = str((file.split("/"))[-1])
            root.title(f"{file_name} - AmTCD")
            field.delete(1.0, END)
            field.insert(1.0, encrypt(text, keyP, keyK))
            field.mark_set("insert", "1.0")
            initial_text = str(field.get("1.0", END))
            is_saved = True
            file_is_created = True
    cancelling = False
    save_dialog_closed = False

def copy_selected():
    global selected_text
    if selected_text is not None:
        root.clipboard_clear()
        root.clipboard_append(selected_text)

def paste_from_clipboard(e=None):
    text = root.clipboard_get()
    field.insert("insert", text)
    check_unsaved()

def ask_for_save():
    global cancelling
    global save_dialog_closed
    save_dialog_closed = False
    choice = askforsave(root, file_name)
    if choice is True:
        save_file()
    if choice is False:
        return
    else:
        cancelling = True
    
def on_closing(e=None):
    global is_saved
    global cancelling
    global save_dialog_closed
    if not is_saved: ask_for_save()
    if not cancelling and not save_dialog_closed: root.destroy()
    cancelling = False
    save_dialog_closed = False

def on_selection(e=None):
    global selected_text
    if field.tag_ranges("sel"):
        start = field.index("sel.first")
        end = field.index("sel.last")
        selected_text = field.get(start, end)
        edit_menu.entryconfig(0, state="normal")
    else:
        edit_menu.entryconfig(0, state="disabled")
        selected_text = None

def update_clipboard_status(e=None):
    global previous_clipboard_state
    try:
        root.clipboard_get()
        if not previous_clipboard_state:
            edit_menu.entryconfig(1, state="normal")
            previous_clipboard_state = True
    except:
        if previous_clipboard_state:
            edit_menu.entryconfig(1, state="disabled")
            previous_clipboard_state = False
    root.after(400, update_clipboard_status)

file_name = "Безымянный"
file_path = None
selected_text = None

config = ConfigParser()
config.read("AmTCD.ini")

keyP = int(config.get("main", "keyuser"))  
keyK = 509

is_saved = True # Маркер. Говорит о том, сохранен ли файл
file_is_created = False # Маркер. Говорит о том, существует ли уже файл на диске
cancelling = False # Маркер. Говорит о том, была ли нажата кпопка "отмена" в диалоге askforsave, или же окно было закрыто
save_dialog_closed = False # Маркер. Говорит о том, было ли закрыто окно файлового диалога при сохранении файла
info_opened = False # Маркер. Говорит о том, открыто ли окно "справка/содержание"

root = Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.title(f"{file_name} - AmTCD")
root.geometry(f"{INITIAL_WIDTH}x{INITIAL_HEIGHT}")
root.config(bg="white")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

width = INITIAL_WIDTH
height = INITIAL_HEIGHT

x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

scrollX = Scrollbar(root, orient=HORIZONTAL) # Горизонтальный скроллбар
scrollX.pack(side=BOTTOM, fill=X)

scrollY = Scrollbar(root) # Вертикальный скроллбар
scrollY.pack(side=RIGHT, fill=Y)

field = Text(bd=0, padx=4 * (current_font_size / DEFAULT_FONT_SIZE), wrap='none', yscrollcommand=scrollY.set, xscrollcommand=scrollX.set,
                  spacing1=0, font=f"Consolas {current_font_size}", insertofftime=500) # Текстовое поле
field.focus()
field.pack(expand=TRUE, fill=BOTH)
field.config(insertborderwidth=100)

# Установка команд для обоих скроллбаров
scrollX.config(command=field.xview) 
scrollY.config(command=field.yview)

initial_text = str(field.get("1.0", END))

mainmenu = Menu(root)
root.config(menu=mainmenu)
file_menu = Menu(mainmenu)
edit_menu = Menu(mainmenu)
info_menu = Menu(mainmenu)
file_menu["tearoff"] = FALSE
edit_menu["tearoff"] = FALSE
info_menu["tearoff"] = FALSE
mainmenu.add_cascade(label="Файл", menu=file_menu)
mainmenu.add_cascade(label="Правка", menu=edit_menu)
mainmenu.add_cascade(label="Справка", menu=info_menu)

file_menu.add_command(label="Новый", activebackground="#91c9f7", activeforeground="black", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Открыть", activebackground="#91c9f7", activeforeground="black", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Сохранить", activebackground="#91c9f7", activeforeground="black", command=save_file, accelerator="Ctrl+S")   
file_menu.add_command(label="Сохранить как...", activebackground="#91c9f7", activeforeground="black", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Выход", activebackground="#91c9f7", activeforeground="black", command=on_closing, accelerator="Ctrl+Q")
edit_menu.add_command(label="Копировать", activebackground="#91c9f7", activeforeground="black", state="disabled",
                           command=copy_selected, accelerator="Ctrl+C")
edit_menu.add_command(label="Вставить", activebackground="#91c9f7", activeforeground="black", state="disabled",
                           command=paste_from_clipboard, accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Параметры...", activebackground="#91c9f7", activeforeground="black", command=change_color_theme)
info_menu.add_command(label="Содержание", activebackground="#91c9f7", activeforeground="black", command=pop_info)
info_menu.add_separator()
info_menu.add_command(label="О программе...", activebackground="#91c9f7", activeforeground="black", command=pop_about)

# Изменение размера шрифта комбинацией Ctrl + Колесо мыши
root.bind("<Control-MouseWheel>", change_scale)
root.bind("<Control-0>", set_default_scale)
# Проверить текст на наличие несохраненных изменений
root.bind("<Key>", check_unsaved)
# Выход из программы
root.bind("<Control-q>", on_closing)
root.bind("<Control-Q>", on_closing)
# Создание нового файла
root.bind("<Control-n>", new_file)
root.bind("<Control-N>", new_file)
# Открытие существующего файла
root.bind("<Control-o>", open_file)
root.bind("<Control-O>", open_file)
# Сохранение файла
root.bind("<Control-s>", save_file)
root.bind("<Control-S>", save_file)
# Выделение текста
field.bind("<<Selection>>", on_selection)

try:
    root.clipboard_get()
    previous_clipboard_state = True
    edit_menu.entryconfig(1, state="normal")
except:
    previous_clipboard_state = False
    edit_menu.entryconfig(1, state="disabled")

update_clipboard_status()

icon = PhotoImage(file=r"icons/notepad.png")
root.iconphoto(False, icon)
root.mainloop()