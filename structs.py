import random


class Word:

    def __init__(self, word, start, direction):
        self.word = word
        self.start = start
        self.direction = direction

    def get_direction_vector(self, multiplier=1):
        if self.direction == 0:
            return 0, -1 * multiplier
        elif self.direction == 1:
            return 1 * multiplier, -1 * multiplier
        elif self.direction == 2:
            return 1 * multiplier, 0
        elif self.direction == 3:
            return 1 * multiplier, 1 * multiplier
        elif self.direction == 4:
            return 0, 1 * multiplier
        elif self.direction == 5:
            return -1 * multiplier, 1 * multiplier
        elif self.direction == 6:
            return -1 * multiplier, 0
        elif self.direction == 7:
            return -1 * multiplier, -1 * multiplier

    def get_end(self):
        v = self.get_direction_vector(len(self.word) - 1)
        return self.start[0] + v[0], self.start[1] + v[1]


class Crossword:
    DIRECTIONS = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))

    def __init__(self, words, x_size, y_size):
        self.words = []
        self.words_to_guess = []
        self.x_size = x_size
        self.y_size = y_size
        self.crossword = []
        self.solution_coords = []
        self.solution = None
        self.solution_start = None
        for i in range(y_size):
            self.crossword.append([])
            for j in range(x_size):
                self.crossword[i].append('')
        for word in words:
            self.add_word(word)

    def set_solution(self, solution):
        self.solution_coords = []
        self.solution = solution
        pos = [self.x_size - 1, self.y_size - 1]
        end = False
        for i in range(len(solution), 0, -1):
            c = solution[i - 1:i]
            if c.upper() == c.lower():
                continue
            while True:
                if pos[0] < 0:
                    pos[0] = self.x_size - 1
                    pos[1] -= 1
                    if pos[1] < 0:
                        end = True
                        break
                if self.crossword[pos[1]][pos[0]] == '':
                    self.crossword[pos[1]][pos[0]] = c.upper()
                    self.solution_coords.append((pos[0], pos[1]))
                    break
                pos[0] -= 1
            if end:
                self.solution_start = solution[0:i] + '...'
                break

    def add_word(self, word):
        pos = [word.start[0], word.start[1]]
        move = word.get_direction_vector()
        errors = []
        end = word.get_end()
        if 0 <= end[0] < self.x_size and 0 <= end[1] < self.y_size:
            for c in word.word:
                if self.crossword[pos[1]][pos[0]] != '' and self.crossword[pos[1]][pos[0]] != c:
                    errors.append((pos, c, self.crossword[pos[1]][pos[0]]))
                pos[0] += move[0]
                pos[1] += move[1]
            if len(errors) != 0:
                raise ValueError('Word cannot be inserted here', word.word, errors)
            pos = [word.start[0], word.start[1]]
            for c in word.word:
                if self.crossword[pos[1]][pos[0]] == '':
                    self.crossword[pos[1]][pos[0]] = c
                pos[0] += move[0]
                pos[1] += move[1]
            self.words.append(word)
            self.words_to_guess.append(word)
        else:
            raise IndexError('Word is too long to be inserted here', word.word)

    @staticmethod
    def save(name, crossword):
        with open('assets/crosswords/' + name + '.cw', 'w', encoding='UTF-8') as cf:
            cf.write(str(crossword.x_size) + ' ' + str(crossword.y_size) + '\n')
            for word in crossword.words:
                cf.write(
                    word.word + ' ' + str(word.start[0]) + ' ' + str(word.start[1]) + ' ' + str(word.direction) + '\n')

    @staticmethod
    def load(name):
        ws = []
        with open('assets/crosswords/' + name + '.cw', encoding='UTF-8') as cf:
            sizes = cf.readline().split(' ')
            lines = cf.readlines()
            for line in lines:
                data = line.split(' ')
                ws.append(Word(data[0], (int(data[1]), int(data[2])), int(data[3])))
        return Crossword(ws, int(sizes[0]), int(sizes[1]))

    @staticmethod
    def load_random_solution():
        with open('assets/crosswords/solutions.txt', encoding='UTF-8') as sf:
            solutions = sf.readlines()
            solution = random.choice(solutions).strip()
        return solution
