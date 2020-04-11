import pygame
import random
import os
import pickle
import sys

x = 250
y = 20
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)  # задаем положение окна

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# index 0 - 6 represent shape

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
# blue = (0, 0, 255)
blue = (65, 105, 225)
yellow = (255, 255, 0)
gold = (255, 215, 0)
silver = (192, 192, 192)

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class Menu:
    def __init__(self):  # иницилиазция меню с выводом заставки
        screen.fill((128, 128, 128))
        self.draw_text(2, 'TETRIS', "comicsans", 90, gold, 190)
        self.draw_text(2, 'Game by developed Nikita Petrushin', "comicsans", 30, gold, 430)
        self.draw_text(2, 'Original idea by Alexey Pajitnov', "comicsans", 30, gold, 455)
        pygame.display.update()
        pygame.display.set_caption('Tetris')
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)  # добавляем иконку
        #pygame.time.delay(2000)

    def draw_text(self, type, message, textFont, textSize, textColor, x):
        font = pygame.font.SysFont(textFont, textSize)
        if type == 0:  # для значения в таблице рекордов
            text = font.render(message, 1, black)
            screen.blit(text, (int(s_width / 2) - int(text.get_width() / 2)
                               + 100 + 2, x + 2))  # "+100" используется для сдвига значений право
            text = font.render(message, 1, textColor)
            screen.blit(text, (int(s_width / 2) - int(text.get_width() / 2) + 100, x))
            return
        if type == 1:  # для имени в таблице рекордов
            text = font.render(message + ":", 1, black)
            screen.blit(text, (int(s_width / 2) - int(text.get_width() / 2)
                               - 100 + 2, x + 2))  # "-100" используется для сдвига имен влево
            text = font.render(message + ":", 1, textColor)
            screen.blit(text, (int(s_width / 2) - int(text.get_width() / 2) - 100, x))
            return
        if type == 2:  # для меню
            text = font.render(message, 1, black)
            screen.blit(text, (int(s_width / 2) - int(text.get_width() / 2) + 2, x + 2))
            text = font.render(message, 1, textColor)
            screen.blit(text, (int(s_width / 2) - int(text.get_width() / 2), x))
        if type == 3:  # для правил
            text = font.render(message, 1, black)
            screen.blit(text, (s_width - 750 + 1, x + 1))
            text = font.render(message, 1, textColor)
            screen.blit(text, (s_width - 750, x))

    def pause(self):  # функция паузы для меню
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    # quit()
                if event.type == pygame.KEYDOWN:
                    return

    def start(self, screen):
        menu = True
        # clock = pygame.time.Clock()
        items = ("START", "RULES", "RECORDS", "QUIT")
        hint = ("Start a new game", "Look up the rules of the game", "Look at the record-breakers",
                "Tap to quit the game")
        i = 0
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    # quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if i > 0:
                            i -= 1
                    elif event.key == pygame.K_DOWN:
                        if i < len(items) - 1:
                            i += 1
                    if event.key == pygame.K_RETURN:
                        selected = items[i]
                        if selected == "START":
                            main(screen)
                        if selected == "RULES":
                            self.rules()
                        if selected == "RECORDS":
                            self.records()
                        elif selected == "QUIT":
                            pygame.quit()
                            sys.exit()
                            # quit()

            # Main Menu UI
            screen.fill(blue)
            selected = items[i]

            self.draw_text(2, 'Tetris', "comicsans", 90, gold, 90)  # заголовок
            for item in items:
                if item == selected:
                    self.draw_text(2, item, "comicsans", 75,
                                   silver, 300 + 60 * items.index(item))  # смена цвета для выбранного значения меню
                    self.draw_text(2, (hint[items.index(item)]), "comicsans", 30, silver, 600)  # вывод подсказки
                else:
                    self.draw_text(2, item, "comicsans", 75,
                                   gray, 300 + 60 * items.index(item))  # отрисовка остального меню

            pygame.display.update()
            # clock.tick()
            # pygame.display.set_caption("Tetris")  # повторение, если неактивна инициализация

    def records(self):
        screen.fill(blue)
        score = Score()
        score_list = score.get_data()
        score_list.sort()
        for i in score_list:
            for j in range(2):
                self.draw_text(j, str(i[j]), "comicsans", 40, silver, 200 + 60 * score_list.index(i))
        self.draw_text(2, "Press ESC to exit", "comicsans", 30, silver, 600)
        pygame.display.update()
        self.pause()

    def rules(self):

        # s = Score()
        # s.update(30)

        screen.fill(blue)
        with open("rules.txt") as f:
            for i, line in enumerate(f):
                self.draw_text(3, line[0:len(line) - 1], "comicsans", 30, silver, 100 + 30 * i)
        self.draw_text(2, "Press ESC to exit", "comicsans", 30, silver, 600)
        pygame.display.update()
        self.pause()


class InputBox:

    def __init__(self, x, y, w, h, text=''):

        self.rect = pygame.Rect(int(x), int(y), w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.empty = False

    def handle_event(self, event):
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            '''

        # if event.type == pygame.QUIT:
        #   pygame.quit()

        if not self.active:
            self.active = True
            self.text = ""
            self.color = COLOR_ACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN:
                    # print(self.text)
                    if not self.text == "":
                        return True, str(self.text)
                    else:
                        self.empty = True
                # elif event.key == pygame.K_ESCAPE:
                #    self.active = False
                #   self.text = ""
                #  self.color = COLOR_INACTIVE
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.rect.w < 250:
                        self.text += event.unicode
                # Re-render the text.
                if self.empty:
                    self.txt_surface = FONT.render("Empty?", True, self.color)
                    self.empty = False
                else:
                    self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Press ESC to exit", 1, black)
        screen.blit(text, (int(s_width / 2) - int(text.get_width() / 2) + 2, 602))
        text = font.render("Press ESC to exit", 1, white)
        screen.blit(text, (int(s_width / 2) - int(text.get_width() / 2), 600))

        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Piece:  # Класс фигуры
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


class Grid:
    def __init__(self, locked_pos={}):
        self.grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j, i) in locked_pos:
                    c = locked_pos[(j, i)]
                    self.grid[i][j] = c
        # return grid

    def valid_space(self, shape):  # проверка доступного места
        accepted_pos = [[(j, i) for j in range(10) if self.grid[i][j] == (0, 0, 0)] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        formatted = convert_shape_format(shape)

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def draw_grid(self, surface):  # отрисовка сетки
        sx = top_left_x
        sy = top_left_y

        for i in range(len(self.grid)):
            pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size),
                             (sx + play_width, sy + i * block_size))
            for j in range(len(self.grid[i])):
                pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                                 (sx + j * block_size, sy + play_height))

    def clear_rows(self, locked):  # удаление полных линий
        inc = 0
        for i in range(len(self.grid) - 1, -1, -1):
            row = self.grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j, i)]
                    except:
                        continue

        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)

        return inc


class Surface:
    def __init__(self, screen):
        self.surface = screen

    def before_exit(self):
        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height / 2 - 100
        self.surface.fill((gray))
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Press Enter if you really want to leave', 1, silver)
        self.surface.blit(label, (int(s_width / 2) - int(label.get_width() / 2), int(sy + 10)))
        label = font.render('Press ESC to continue', 1, silver)
        self.surface.blit(label, (int(s_width / 2) - int(label.get_width() / 2), int(sy + 70)))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return False
                    if event.key == pygame.K_ESCAPE:
                        return True


    def draw_text_middle(self, text, size, color):  # отрисовка надписи в центре
        font = pygame.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, 1, color)

        self.surface.blit(label, (int(top_left_x + play_width / 2 - (label.get_width() / 2)),
                                  int(top_left_y + play_height / 2 - label.get_height() / 2)))  # выводим на экран

    def draw_next_shape(self, shape):  # отрисовка следующей фигуры
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, silver)

        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height / 2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(self.surface, shape.color,
                                     (int(sx + j * block_size), int(sy + i * block_size), block_size, block_size), 0)

        self.surface.blit(label, (int(sx + 10), int(sy - 30)))

    def draw_window(self, grid, score=0, last_score=0):
        self.surface.fill((0, 0, 0))

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Tetris', 1, silver)

        self.surface.blit(label, (int(top_left_x + play_width / 2 - (label.get_width() / 2)), 30))

        # current score
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Score: ' + str(score), 1, silver)

        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height / 2 - 100

        self.surface.blit(label, (int(sx + 20), int(sy + 160)))

        # last score
        label = font.render('High Score: ' + last_score, 1, silver)

        sx = top_left_x - 200
        sy = top_left_y + 200

        self.surface.blit(label, (sx + 20, sy + 160))

        # pause hint
        label = font.render('Press P to pause', 1, silver)
        self.surface.blit(label, (sx - 5 , sy - 30))

        label = font.render('Press Space to drop', 1, silver)
        self.surface.blit(label, (sx - 5 , sy - 10))

        label = font.render('Use arrows to move', 1, silver)
        self.surface.blit(label, (sx - 5, sy + 10))

        for i in range(20):
            for j in range(10):
                pygame.draw.rect(self.surface, grid.grid[i][j],
                                 (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

        pygame.draw.rect(self.surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

        grid.draw_grid(self.surface)
        # pygame.display.update()


class Score:  # Класс рекордов
    def __init__(self):
        self.new_name = []

    def find_max(self):
        with open('scores.txt', 'rb') as f:
            l_in = pickle.load(f)
        return str(max(l_in)[0])

    def read_name(self):
        input_box1 = InputBox(s_width / 2 - (200 / 2), 300, 140, 32, "Enter your name")
        # input_box2 = InputBox(100, 300, 140, 32)
        # input_boxes = [input_box1, input_box2]
        input_boxes = [input_box1]

        for _ in input_boxes:
            self.new_name.append("")

        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    for box in input_boxes:
                        event_result = box.handle_event(event)
                        if event_result is not None:
                            if not event_result:
                                return done
                            if event_result[0]:
                                self.new_name[input_boxes.index(box)] = box.handle_event(event)[1]
                                done = True  # можно упростить, но не буду
                                return done

            for box in input_boxes:
                box.update()

            screen.fill((30, 30, 30))
            for box in input_boxes:
                box.draw(screen)
            pygame.display.update()

    def get_data(self):
        with open('scores.txt', 'rb') as f:
            l_in = pickle.load(f)
        return l_in

    def update(self, nscore):
        rec_list = self.get_data()
        if nscore >= min(rec_list)[0]:

            if not self.read_name():
                return  # выход, если read_name вернул False

            rec_list.sort();
            rec_list[0][0] = nscore
            rec_list[0][1] = self.new_name[0]

            with open('scores.txt', 'wb') as out:
                pickle.dump(rec_list, out)


def convert_shape_format(shape):  # преобразование массива в фигуру
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def check_lost(positions):  # проверка: проиграл ли пользователь или нет
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():  # получение случайной фигуры
    return Piece(5, 0, random.choice(shapes))


def main(screen):  # главный метод
    surface = Surface(screen)
    score = Score()
    last_score = score.find_max()
    locked_positions = {}
    # grid = create_grid(locked_positions)

    change_piece = False  # смена фигуры на следующую
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    temp_score = 0

    while run:
        grid = Grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005  # увеличение скорости

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (grid.valid_space(current_piece)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = surface.before_exit()
                   # run = False

                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (grid.valid_space(current_piece)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (grid.valid_space(current_piece)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (grid.valid_space(current_piece)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (grid.valid_space(current_piece)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_SPACE:
                    while grid.valid_space(current_piece):
                        current_piece.y += 1
                    current_piece.y -= 1
                if event.key == pygame.K_p:
                    pause = True
                    while pause:
                        for pause_event in pygame.event.get():
                            surface.draw_text_middle("PAUSE", 80, silver)
                            pygame.display.update()
                            if pause_event.type == pygame.QUIT:
                                run = False
                                pygame.display.quit()
                                sys.exit()
                            if pause_event.type == pygame.KEYDOWN:
                                if pause_event.key == pygame.K_p:
                                    pause = False

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid.grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            temp_score += grid.clear_rows(locked_positions) * 10

        surface.draw_window(grid, temp_score, last_score)
        surface.draw_next_shape(next_piece)
        pygame.display.update()

        if check_lost(locked_positions):
            surface.draw_text_middle("YOU LOST!", 80, silver)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            score.update(temp_score)


screen = pygame.display.set_mode((s_width, s_height))  # создаем окно
menu = Menu()
menu.start(screen)  # запускаем меню
