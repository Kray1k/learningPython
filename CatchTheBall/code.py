#!/usr/bin/env python
# -*- coding: utf-8 -*

import pygame
from pygame.draw import *
from random import randint

FPS = 60
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Catch The Ball')
validChars = "`1234567890-=qwertyuiopasdfghjkl'zxcvbnm,./ \
    абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
shiftChars = '~!@#$%^&*()_+QWERTYUIOPASDFGHJKL"ZXCVBNM<>? \
    АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
shiftDown = False

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = (RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.r = int(randint(32, 64))
        self.color = COLORS[randint(0, 5)]
        self.velocity = randint(2, 8)
        self.image = pygame.Surface((self.r, self.r), pygame.SRCALPHA)
        circle(self.image, self.color, (self.r//2, self.r//2), self.r//2)
        self.pos = pygame.math.Vector2(randint(100, screen.get_width() - 100),
                                       randint(100, screen.get_height() - 100))
        self.rect = self.image.get_rect(center = self.pos)
        self.dir = pygame.math.Vector2(self.pos).normalize()
        self.rect = self.image.get_rect(center = (round(self.pos.x),
                                                  round(self.pos.y)))
        self.timer = FPS * randint(1, 6)
        self.init_timer = self.timer // FPS

    def get_points(self):
        points = 1;
        if self.velocity > 4:
            points += 1
        if self.r < 48:
            points += 1
        if self.init_timer - self.timer/FPS < 1:
            points += 1
        return points

    def reflect(self, NV):
        self.dir = self.dir.reflect(pygame.math.Vector2(NV))

    def update(self):
        self.pos += self.dir * self.velocity
        self.rect.center = self.pos
        if self.rect.left <= 0:
            self.reflect((1, 0))
            self.rect.left = 0
        if self.rect.right >= screen.get_width():
            self.reflect((-1, 0))
            self.rect.right = screen.get_width()
        if self.rect.top <= 0:
            self.reflect((0, 1))
            self.rect.top = 0
        if self.rect.bottom >= screen.get_height():
            self.reflect((0, -1))
            self.rect.bottom = screen.get_height()
        self.timer -= 1

    def mouse_in_ball(self, event) -> bool:
        if ((event.pos[0]-self.pos[0])**2 +
            (event.pos[1]-self.pos[1])**2 <= (self.r/2)**2):
            return True
        return False


class Player:
    def __init__(self, name):
        self.__name = name
        self.__points = 0

    def add_points(self, count):
        self.__points += count

    def get_points(self) -> int:
        return self.__points

    def get_name(self) -> str:
        return self.__name

    def remove_points(self, count):
        if self.__points <= 0 or self.__points - count <= 0:
            self.points = 0
        else:
            self.__points -= count


class TextBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        pygame.font.init()
        self.font = pygame.font.Font(None, 50)
        self.image = self.font.render("Введите имя игрока", False, [255, 255, 255])
        self.rect = self.image.get_rect()

    def add_chr(self, char):
        global shiftDown
        if char in validChars:
            if shiftDown:
                self.text += shiftChars[validChars.index(char)]
            else:
                self.text += char
        self.update()

    def update(self):
        old_rect_pos = self.rect.center
        self.image = self.font.render(self.text, False, [255, 255, 255])
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_pos


def reflectBalls(ball_1, ball_2):
    v1 = pygame.math.Vector2(ball_1.rect.center)
    v2 = pygame.math.Vector2(ball_2.rect.center)
    r1 = ball_1.r//2
    r2 = ball_2.r//2
    d = v1.distance_to(v2)
    if d < r1 + r2 - 2:
        dnext = (v1 + ball_1.dir).distance_to(v2 + ball_2.dir)
        nv = v2 - v1
        if dnext < d and nv.length() > 0:
            ball_1.reflect(nv)
            ball_2.reflect(nv)

def newScoreToFile(name, newScore):
    scores = list()
    txt = None
    try: 
        txt = open('scores.txt', 'r')
        txt.readline()
        while True:
            inp = txt.readline()
            if inp:
                scores.append(list(inp.split(': ')))
                scores[-1][0] = scores[-1][0].split('. ')[1]
                scores[-1][1] = scores[-1][1].replace('\n', '')
            else:
                break
        scores.append([name, newScore])
        scores.sort(key=lambda l: int(l[1]), reverse=True)
        scores2 = [scores[0]]
        for name, score in scores:
            if name != scores2[-1][0]:
                scores2.append([name, score])
        scores = scores2
        txt.close()
        txt = open('scores.txt', 'w')
    except FileNotFoundError:
        txt = open('scores.txt', 'w')
        scores.append([name,newScore])
    txt.write('Список набранных игроками очков')
    for i, score in enumerate(scores, start=1):
        txt.write('\n' + str(i) + '. ' + score[0] + ': ' + str(score[1]))
    txt.close()


def main():
    clock = pygame.time.Clock()
    running = True
    pygame.init()
    pygame.display.flip()
    textBox = TextBox()
    textBox.rect.center = [screen.get_width()//2, screen.get_height()//2]
    global shiftDown
    while running:
        clock.tick(FPS)
        screen.fill([0, 0, 0])
        screen.blit(textBox.image, textBox.rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    shiftDown = False
            if event.type == pygame.KEYDOWN:
                textBox.add_chr(pygame.key.name(event.key))
                if event.key == pygame.K_SPACE:
                    textBox.text += " "
                    textBox.update()
                if event.key in [pygame.K_LSHIFT, pygame.K_LSHIFT]:
                    shiftDown = True
                if event.key == pygame.K_BACKSPACE:
                    textBox.text = textBox.text[:-1]
                    textBox.update()
                if event.key == pygame.K_RETURN:
                    if len(textBox.text) > 0:
                        running = False
    running = True
    player = Player(textBox.text)
    spawn_time = int(FPS*0.5)
    balls = pygame.sprite.Group()
    balls.add(Ball(), Ball(), Ball())
    while running:
        clock.tick(FPS)
        balls.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for ball in balls:
                    if ball.mouse_in_ball(event):
                        player.add_points(ball.get_points())
                        balls.remove(ball)
        balls_list = balls.sprites()
        for i, ball1 in enumerate(balls_list[:-1]):
            for ball2 in balls_list[i+1:]:
                reflectBalls(ball1, ball2)
        for ball in balls:
            if ball.timer == 0:
                balls.remove(ball)
                player.remove_points(1)
        balls.draw(screen)
        pygame.display.flip()
        screen.fill(BLACK)
        spawn_time -= 1
        if spawn_time == 0:
            balls.add(Ball())
            spawn_time = int(FPS*0.5)
    textBox.text = ("Игрок " + str(player.get_name()) + ": " +
                    str(player.get_points()) + " очков")
    newScoreToFile(player.get_name(), player.get_points())
    textBox.update()
    running = True
    while running:
        clock.tick(FPS)
        screen.fill([0, 0, 0])
        screen.blit(textBox.image, textBox.rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    running = False
    pygame.quit()

if __name__ == "__main__":
    main()
