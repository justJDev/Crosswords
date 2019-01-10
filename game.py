import random, os, tkinter, math
from structs import Crossword
from render import Render
from help import Help
from cwmanager import CWManager


class CrosswordsGame:

    def __init__(self):
        self.current_crossword = None
        self.x_size = 10
        self.y_size = 10
        self.selected = None
        # WINDOW CONFIG
        self.main_window = tkinter.Tk()
        self.main_window.resizable(False, False)
        self.main_window.title('Osemsmerovky')
        # CANVAS CONFIG
        self.canvas = tkinter.Canvas(self.main_window, height=360, width=720)
        self.canvas.pack(side='bottom')
        self.canvas.bind('<Button-1>', self.select)
        self.canvas.bind('<Button-3>', lambda e: self.end_selection((-1, -1)))
        # HELP BUTTON
        tkinter.Button(self.main_window, text='? (F1)', command=self.show_help).pack(side='right', anchor='ne')
        self.main_window.bind('<F1>', lambda e: self.show_help())
        # NEW GAME BUTTON
        tkinter.Button(self.main_window, text='Nová hra (N)', command=self.new_game).pack(side='left', anchor='nw')
        self.main_window.bind('<n>', lambda e: self.new_game())
        # CW MANAGER BUTTON
        tkinter.Button(self.main_window, text='Moje osemsmerovky (M)', command=lambda: CWManager.show(self)).pack(
            side='right', anchor='nw')
        self.main_window.bind('<m>', lambda e: CWManager.show(self))
        # COORDINATES TOGGLE
        self.main_window.bind('<c>', lambda e: self.toggle_coordinates())

    def new_game(self):
        self.load_random_crossword()

    def load_crossword(self, name):
        crossword = Crossword.load(name)
        if len(crossword.words) == 0:
            print('Empty crossword found:', name)
            self.new_game()
            return
        crossword.set_solution(Crossword.load_random_solution())
        self.current_crossword = crossword
        self.draw(self.current_crossword)

    def load_default_crossword(self):
        self.load_crossword('builtin-cw01')

    def load_random_crossword(self):
        cws = []
        for file in os.listdir('assets/crosswords'):
            if file.endswith('.cw'):
                cws.append(file.replace('.cw', ''))
        self.load_crossword(random.choice(cws))

    def select_word(self, start, end):
        word_found = None
        for word in self.current_crossword.words_to_guess:
            if word.start == start and word.get_end() == end or word.start == end and word.get_end() == start:
                word_found = word
                break
        if word_found:
            self.current_crossword.words_to_guess.remove(word_found)
            self.cross_word(start, end, self.current_crossword.words.index(word_found))
            if len(self.current_crossword.words_to_guess) == 0:
                self.won(self.current_crossword.solution, self.current_crossword.solution_coords)

    def draw(self, crossword):
        self.x_size = crossword.x_size
        self.y_size = crossword.y_size
        w1 = math.ceil(len(crossword.words) / self.y_size) * 100 + self.x_size * 20 + 40
        w2 = len(crossword.solution) * 10 + 40
        self.canvas.config(width=w1 if w1 > w2 else w2, height=self.y_size * 20 + 80)
        self.canvas.delete('all')
        Render.draw_table(self.canvas, crossword)
        Render.draw_letters(self.canvas, crossword)
        Render.draw_words(self.canvas, crossword)
        self.canvas.create_text(10, self.y_size * 20 + 20, text=crossword.solution_start, anchor='nw', font='Arial 16',
                                tag='solution')

    def select(self, event):
        if 10 < event.x < self.x_size * 20 + 10 and 10 < event.y < self.y_size * 20 + 10:
            pos = ((event.x - 10) // 20, (event.y - 10) // 20)
            if self.selected and self.validate_selection(pos):
                self.end_selection(pos)
            else:
                self.start_selection(pos)

    def start_selection(self, pos):
        self.canvas.delete('selection')
        self.canvas.delete('selection_start')
        self.selected = pos
        self.canvas.create_rectangle(pos[0] * 20 + 10, pos[1] * 20 + 10, pos[0] * 20 + 30, pos[1] * 20 + 30,
                                     fill='green', tag='selection_start')
        for d in Crossword.DIRECTIONS:
            x, y = pos[0], pos[1]
            while x in range(self.x_size) and y in range(self.y_size):
                x += d[0]
                y += d[1]
                if x in range(self.x_size) and y in range(self.y_size):
                    self.canvas.create_rectangle(x * 20 + 10, y * 20 + 10, x * 20 + 30, y * 20 + 30, fill='orange',
                                                 tag='selection')
        self.canvas.tag_lower('selection')
        self.canvas.tag_lower('selection_start')
        self.canvas.tag_lower('line')

    def end_selection(self, pos):
        self.select_word(self.selected, pos)
        self.canvas.delete('selection')
        self.canvas.delete('selection_start')
        self.selected = None

    def validate_selection(self, end, start=None):
        if not start:
            start = self.selected
        return start[0] == end[0] or start[1] == end[1] or abs(start[0] - end[0]) == abs(start[1] - end[1])

    def cross_word(self, start, end, index):
        self.canvas.create_line(start[0] * 20 + 20, start[1] * 20 + 20, end[0] * 20 + 20, end[1] * 20 + 20, tag='line',
                                fill='red')
        i = index % self.y_size
        j = index // self.y_size
        self.canvas.create_line(j * 100 + self.x_size * 20 + 20, i * 20 + 20, j * 100 + self.x_size * 20 + 20 + 90,
                                i * 20 + 20)
        self.canvas.tag_lower('line')

    def won(self, solution, solution_coords):
        for pos in solution_coords:
            self.canvas.create_rectangle(pos[0] * 20 + 10, pos[1] * 20 + 10, pos[0] * 20 + 30, pos[1] * 20 + 30,
                                         fill='#00FF00', tag='solution_letter')
        self.canvas.tag_lower('solution_letter')
        self.canvas.delete('solution')
        self.canvas.create_text(10, self.y_size * 20 + 20, text=solution, anchor='nw', font='Arial 16', tag='solution')
        self.canvas.create_text(10, self.y_size * 20 + 50, text='Gratulujem, našli ste všetky slová!', anchor='nw',
                                font='Arial 18')

    def show_help(self):
        Help.show(self.main_window)
        self.main_window.wait_window(Help.help_window)

    def toggle_coordinates(self):
        if self.canvas.find_withtag('coords'):
            self.canvas.delete('coords')
        else:
            for i in range(self.x_size):
                self.canvas.create_text(i * 20 + 20, 5, text=i, font='Arial 7', tag='coords')
                for j in range(self.y_size):
                    self.canvas.create_text(5, j * 20 + 20, text=j, font='Arial 7', tag='coords')

