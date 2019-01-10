import tkinter, secrets, os
from tkinter import messagebox
from generator import Generator


class CWManager:
    window = None
    cw_list = None
    h_entry = None
    w_entry = None
    game = None

    @staticmethod
    def show(game):
        try:
            CWManager.window.lift()
            CWManager.window.focus_force()
        except:
            CWManager.window = tkinter.Tk()
            CWManager.window.title('Moje osemsmerovky')
            CWManager.window.resizable(False, False)
            CWManager.window.lift()
            CWManager.window.focus_force()
            CWManager.window.bind('<Escape>', lambda e: CWManager.close())
            # USER CREATED CROSSWORD LIST
            CWManager.cw_list = tkinter.Listbox(CWManager.window, width=50)
            CWManager.cw_list.pack(side='top')
            CWManager.cw_list.bind('<Double-Button-1>', CWManager.play_crossword)
            # EDIT CROSSWORD
            tkinter.Button(CWManager.window, text='Upraviť vybranú osemsmerovku',
                           command=CWManager.edit_crossword).pack(side='top')
            # DELETE CROSSWORD
            tkinter.Button(CWManager.window, text='Zmazať vybranú osemsmerovku',
                           command=CWManager.delete_crossword).pack(side='top')
            # SPACER
            tkinter.LabelFrame(CWManager.window, text='', height='10').pack(side='top')
            # CREATE CROSSWORD UI
            tkinter.Label(CWManager.window, text='Šírka novej osemsmerovky').pack(side='top')
            CWManager.w_entry = tkinter.Entry(CWManager.window)
            CWManager.w_entry.insert(0, '10')
            CWManager.w_entry.pack(side='top')
            tkinter.Label(CWManager.window, text='Výška novej osemsmerovky').pack(side='top')
            CWManager.h_entry = tkinter.Entry(CWManager.window)
            CWManager.h_entry.insert(0, '10')
            CWManager.h_entry.pack(side='top')
            tkinter.Button(CWManager.window, text='Vytvoriť novú osemsmerovku',
                           command=CWManager.create_crossword).pack(
                side='top')
            CWManager.game = game
        CWManager.load_user_crosswords()

    @staticmethod
    def create_crossword():
        name = secrets.token_hex(2)
        try:
            height = CWManager.h_entry.get()
            int(height)
            try:
                width = CWManager.w_entry.get()
                int(width)
                with open('assets/crosswords/user-' + name + '.cw', 'w', encoding='UTF-8') as cwfile:
                    cwfile.write(width.replace('-', '') + ' ' + height.replace('-', ''))
                CWManager.load_user_crosswords()
                CWManager.edit_crossword(name)
            except ValueError:
                messagebox.showerror('Nová osemsmerovka', '\'' + CWManager.w_entry.get() + '\' nie je platné číslo',
                                     parent=CWManager.window)
        except ValueError:
            messagebox.showerror('Nová osemsmerovka', '\'' + CWManager.h_entry.get() + '\' nie je platné číslo',
                                 parent=CWManager.window)

    @staticmethod
    def delete_crossword():
        try:
            name = CWManager.cw_list.get(CWManager.cw_list.curselection())
            if os.path.exists('assets/crosswords/user-' + name + '.cw'):
                os.remove('assets/crosswords/user-' + name + '.cw')
        except:
            pass
        CWManager.load_user_crosswords()

    @staticmethod
    def load_user_crosswords():
        CWManager.cw_list.delete(0, 'end')
        for file in os.listdir('assets/crosswords'):
            if file.startswith('user-') and file.endswith('.cw'):
                CWManager.cw_list.insert('end', file.replace('.cw', '').replace('user-', ''))

    @staticmethod
    def edit_crossword(name=None):
        try:
            if name is None:
                name = CWManager.cw_list.get(CWManager.cw_list.curselection())
            Generator('user-' + name)
        except:
            pass

    @staticmethod
    def play_crossword(e):
        try:
            name = CWManager.cw_list.get(CWManager.cw_list.curselection())
            CWManager.game.load_crossword('user-' + name)
        except:
            pass

    @staticmethod
    def close():
        CWManager.window.destroy()
        CWManager.window = None
