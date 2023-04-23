import sys
from random import randint  # из набора инструментов для создания рандомных чисел берем инструмент для рандомного int

import pygame as pg


class GameLogic:
    def __init__(self, app, max_score=0):
        self.app = app
        self.field_width = self.app.screen.get_width() // 20
        self.field_height = self.app.screen.get_height() // 20
        x = self.field_width // 2
        y = self.field_height // 2 + self.field_height // 4
        self.platform = [[x - 2, y], [x - 1, y], [x, y], [x + 1, y], [x + 2, y]]
        self.ball = [randint(0, self.field_width), y - 5]       ##########################################
        self.ball_dir = [1, -1]      #####################################################################
        self.bricks = [[1] * 5 for _ in range(self.field_width)]
        self.game_over = False
        self.game_won = False       #####################################################################
        self.timer = 0
        self.score = 0
        self.max_score = max_score

    def restart(self):
        x = self.field_width // 2
        y = self.field_height // 2 + self.field_height // 4
        self.platform = [[x - 2, y], [x - 1, y], [x, y], [x + 1, y], [x + 2, y]]
        self.ball = [x, y - 5]
        self.ball_dir = [1, -1]      #####################################################################
        self.bricks = [[1] * 5 for _ in range(self.field_width)]
        self.game_over = False
        self.game_won = False       #####################################################################
        self.timer = 0
        self.score = 0
        print(f'Max score is {self.max_score}!')

    def draw(self):
        self.draw_platform()
        self.draw_ball()
        self.draw_bricks()
        self.draw_score()
        if self.game_over:
            self.draw_game_over()

    def draw_platform(self):
        for index, square in enumerate(self.platform):
            pg.draw.rect(self.app.screen, (150, 0, 150), [square[0] * 20, square[1] * 20, 20, 20])

    def draw_ball(self):
        pg.draw.rect(self.app.screen, (254, 254, 254), [self.ball[0] * 20, self.ball[1] * 20, 20, 20])

    def draw_bricks(self):
        for x in range(self.field_width):
            for y in range(5):
                if self.bricks[x][y] == 1:
                    if (x + 1) % 4 != 0:
                        pg.draw.rect(self.app.screen, (100, 2, 50 * (y + 1)), [x * 20, (y + 3) * 20, 20, 20])
                    else:
                        pg.draw.rect(self.app.screen, (100, 100, 50 * (y + 1)), [x * 20, (y + 3) * 20, 20, 20])

    def draw_score(self):
        img = self.app.score_font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.app.screen.blit(img, (10, 10))

    def draw_game_over(self):  # метод прорисовки заставки "Игра окончена"
        img = self.app.score_font.render(f'You lose scoring {self.score}. Max record is {self.max_score}', True,
                                         (255, 0, 0))
        self.app.screen.blit(img, (200, 200))

    def move_left(self):
        if self.platform[0][0] > 0:
            for i in range(5):
                self.platform[i][0] -= 1

    def move_right(self):
        if self.platform[4][0] < self.field_width - 1:
            for i in range(5):
                self.platform[i][0] += 1

    def update(self):       ##################################################
        if self.game_over:
            return

        self.timer += self.app.dt
        delay = 0.07
        if self.timer < delay:
            return
        self.timer -= delay

        new_ball = [self.ball[0] + self.ball_dir[0], self.ball[1] + self.ball_dir[1]]
        if new_ball[0] > self.field_width - 1 or new_ball[0] < 0:       # отскок от стен
            self.ball_dir[0] *= -1
            new_ball[0] = self.ball[0] + self.ball_dir[0]
        if new_ball[1] < 0 or new_ball in self.platform:                # отскок от потолка
            self.ball_dir[1] *= -1
            new_ball[1] = self.ball[1] + self.ball_dir[1]
        if new_ball[1] < 8:                                             # отскок от блоков
            if self.bricks[new_ball[0]][new_ball[1] - 3] == 1:          # если мы столкнемся с блоком
                temp_ball = new_ball.copy()                             # сохраняем рассчитанный мяч
                if self.bricks[self.ball[0]][new_ball[1] - 3] == 1:     # если блок находится над нами
                    self.ball_dir[1] *= -1                              # разворачиваем по вертикали
                    new_ball[1] = self.ball[1] + self.ball_dir[1]       # делаем отскок
                else:                                                   # иначе
                    if self.ball[1] < 8:                                # если мы находимся в области блоков
                        if self.bricks[new_ball[0]][self.ball[1] - 3] == 1:     # если блок сбоку
                            self.ball_dir[0] *= -1                              # разворачиваем по горизонтали
                            new_ball[0] = self.ball[0] + self.ball_dir[0]       # делаем отскок
                        else:                                                   # иначе (то есть мы попали в угол блока)
                            self.ball_dir[0] *= -1                              # разворачиваем по горизонтали
                            self.ball_dir[1] *= -1                              # разворачиваем по вертикали
                            new_ball = self.ball                                # отскока нет (летим противополож. ст.)
                    else:                                           # иначе (то есть мы попали в угол блока)
                        self.ball_dir[0] *= -1                      # разворачиваем по горизонтали1
                        self.ball_dir[1] *= -1                      # разворачиваем по вертикали1
                        new_ball = self.ball                        # отскока нет (летим противополож. ст.)
                for i in range(4):
                    self.bricks[(temp_ball[0] // 4) * 4 + i][temp_ball[1] - 3] = 0
                self.score += 1

        # godmod
        # if self.ball[1] > self.platform[0][1] + 4:
        #     self.ball_dir[1] *= -1
        #     new_ball[1] = self.ball[1] + self.ball_dir[1]

        if self.ball[1] > self.platform[0][1] + 8:
            self.game_over = True
            if self.score > self.max_score:
                self.max_score = self.score

        self.ball = new_ball


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1200, 900))
        pg.display.set_caption('Arkanoid')
        self.clock = pg.time.Clock()
        self.score_font = pg.font.SysFont("exo2extrabold", 24)
        self.dt = 0.0
        self.logic = GameLogic(self)

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()  # прекращаем работу с pygame
                sys.exit()  # закрываем окно
            if self.logic.game_over:  # если игра проиграна (смотри строку №41)
                if e.type == pg.KEYDOWN:  # если какая-то клавиша нажата
                    # TODO: save records
                    self.logic.restart()
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT] or keys[ord('a')]:
                self.logic.move_left()
            if keys[pg.K_RIGHT] or keys[ord('d')]:
                self.logic.move_right()

    def update(self):
        self.logic.update()
        pg.display.flip()
        self.dt = self.clock.tick() * 0.001

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.logic.draw()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


app = App()
app.run()
