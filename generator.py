import tkinter, random, time
from tkinter import messagebox
from threading import Thread
from structs import Crossword, Word
from render import Render


class Generator:

    def __init__(self, name):
        self.progressbar_pos = [0, 0]
        self.progressbar_dir = 'e'
        self.name = name
        self.progressbar_on = False
        self.thread = None
        self.crossword = Crossword.load(name)
        # WINDOW CONFIG
        self.window = tkinter.Tk()
        self.window.title('Generátor osemsmeroviek')
        self.window.resizable(False, False)
        self.window.lift()
        self.window.focus_force()
        self.window.bind('<Escape>', lambda e: self.close())
        self.width = self.crossword.x_size * 20 + 18
        self.height = self.crossword.y_size * 20 + 18
        self.canvas = tkinter.Canvas(self.window, height=self.height, width=self.width)
        self.canvas.pack(side='right')
        Render.draw_table(self.canvas, self.crossword)
        # WORD LIST
        self.word_list = tkinter.Listbox(self.window, width='22')
        self.word_list.pack(side='top', anchor='n')
        for word in self.crossword.words:
            self.word_list.insert('end', word.word)
        if len(self.crossword.words):
            Render.draw_letters(self.canvas, self.crossword)
        tkinter.Button(self.window, text='Zmazať slovo', command=self.delete_selected, width='18').pack(side='top',
                                                                                                        anchor='n')
        # SPACER
        tkinter.LabelFrame(self.window, text='', height='10').pack(side='top')
        # NEW WORD
        self.nw_entry = tkinter.Entry(self.window, width='22')
        self.nw_entry.pack(side='top', anchor='n')
        self.nw_entry.bind('<Return>', lambda e: self.add_word())
        tkinter.Button(self.window, text='Pridať slovo', command=self.add_word, width='18').pack(side='top', anchor='n')
        # SPACER
        tkinter.LabelFrame(self.window, text='', height='12').pack(side='top')
        # GENERATE AND SAVE
        tkinter.Button(self.window, text='Generovať', command=self.generate, width='18').pack(side='top', anchor='s')
        self.save_btn = tkinter.Button(self.window, text='Uložiť', command=self.save, width='18', state='disabled')
        self.save_btn.pack(side='top', anchor='s')

    def add_word(self):
        word = self.nw_entry.get().upper()
        if word:
            self.word_list.insert('end', word)
            self.word_list.yview('end')
            self.nw_entry.delete(0, 'end')
        else:
            messagebox.showerror('Nová osemsmerovka', 'Vstup musí obsahovať slovo', parent=self.window)

    def delete_selected(self):
        try:
            selected = self.word_list.curselection()
            self.word_list.delete(selected)
        except:
            pass

    def generate(self):
        words = list(self.word_list.get(0, 'end'))
        if len(words):
            self.crossword = Crossword([], self.crossword.x_size, self.crossword.y_size)
            self.thread = GeneratorThread(self.crossword, words)
            self.start_progressbar()
            self.thread.start()
        else:
            messagebox.showerror('Generátor osemsmeroviek', 'Musíte vložiť aspoň 1 slovo', parent=self.window)

    def save(self):
        Crossword.save(self.name, self.crossword)
        self.close()

    def start_progressbar(self):
        self.progressbar_pos = [0, 0]
        self.progressbar_dir = 'e'
        self.progressbar_on = True
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='white', outline='white', tag='gen')
        self.canvas.create_text(self.width // 2, self.height // 2, text='Generujem osemsmerovku...', font='Arial 12',
                                tag='gen')
        self.canvas.create_rectangle(0, 0, 10, 10, fill='black', tag='progressbar')
        self.move_progressbar()

    def stop_progressbar(self):
        self.progressbar_on = False
        self.canvas.delete('gen')
        self.canvas.delete('progressbar')

    def move_progressbar(self):
        if self.thread.done:
            self.stop_progressbar()
            if len(self.thread.unplaced_words):
                messagebox.showinfo('Generátor osemsmeroviek',
                                    'Nepodarilo sa umiestniť tieto slová: ' + ', '.join(self.thread.unplaced_words),
                                    parent=self.window)
            Render.draw_letters(self.canvas, self.crossword)
            self.thread = None
            self.save_btn.config(state='normal')
        if self.progressbar_on:
            if self.progressbar_dir == 'e':
                if self.progressbar_pos[0] + 10 >= self.width:
                    self.progressbar_dir = 's'
                else:
                    self.canvas.move('progressbar', 5, 0)
                    self.progressbar_pos[0] += 5
            elif self.progressbar_dir == 's':
                if self.progressbar_pos[1] + 10 >= self.height:
                    self.progressbar_dir = 'w'
                else:
                    self.canvas.move('progressbar', 0, 5)
                    self.progressbar_pos[1] += 5
            elif self.progressbar_dir == 'w':
                if self.progressbar_pos[0] <= 0:
                    self.progressbar_dir = 'n'
                else:
                    self.canvas.move('progressbar', -5, 0)
                    self.progressbar_pos[0] -= 5
            elif self.progressbar_dir == 'n':
                if self.progressbar_pos[1] <= 0:
                    self.progressbar_dir = 'e'
                else:
                    self.canvas.move('progressbar', 0, -5)
                    self.progressbar_pos[1] -= 5
            self.canvas.after(10, func=self.move_progressbar)

    def close(self):
        self.window.destroy()
        self.window = None

    @staticmethod
    def all_positions(w, h):
        pos = []
        for i in range(w):
            for j in range(h):
                pos.append((i, j))
        return pos


class GeneratorThread(Thread):
    def __init__(self, crossword, words):
        Thread.__init__(self)
        self.words = words
        self.crossword = crossword
        self.done = False
        self.unplaced_words = []

    def run(self):
        self.words = sorted(self.words, key=len)[::-1]
        for word in self.words:
            placed = False
            positions = list(Generator.all_positions(self.crossword.x_size, self.crossword.y_size))
            random.shuffle(positions)
            for pos in positions:
                directions = list(range(8))
                random.shuffle(directions)
                for direction in directions:
                    try:
                        self.crossword.add_word(Word(word, pos, direction))
                        placed = True
                        break
                    except:
                        pass
                if placed:
                    break
            if not placed:
                self.unplaced_words.append(word)
        time.sleep(5)  # TO SHOW THE ANIMATION
        self.done = True
