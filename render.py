class Render:

    @staticmethod
    def draw_table(canvas, crossword):
        canvas.delete('table')
        for i in range(crossword.x_size + 1):
            canvas.create_line(i * 20 + 10, 10, i * 20 + 10, crossword.y_size * 20 + 10, tag='table')
            for j in range(crossword.y_size + 1):
                canvas.create_line(10, j * 20 + 10, crossword.x_size * 20 + 10, j * 20 + 10, tag='table')

    @staticmethod
    def draw_letters(canvas, crossword):
        canvas.delete('letter')
        x = y = 0
        for line in crossword.crossword:
            for c in line:
                canvas.create_text(x * 20 + 20, y * 20 + 20, text=c, tag='letter')
                x += 1
            x = 0
            y += 1

    @staticmethod
    def draw_words(canvas, crossword):
        canvas.delete('word')
        i = 0
        j = 0
        for word in crossword.words:
            if i > crossword.y_size - 1:
                i = 0
                j += 1
            canvas.create_text(j * 100 + crossword.x_size * 20 + 20, i * 20 + 20, text=word.word, anchor='w',
                               tag='word')
            i += 1
