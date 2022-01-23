#!/usr/bin/env python
# -*- coding: utf-8 -*

import pygame
from pygame.draw import *
from random import randint

FPS = 25
screen = pygame.display.set_mode((600, 600))

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
        self.velocity = randint(5, 12)
        self.image = pygame.Surface((self.r, self.r), pygame.SRCALPHA)
        circle(self.image, self.color, (self.r//2, self.r//2), self.r//2)
        self.pos = pygame.math.Vector2(randint(100, screen.get_width()),
                                       randint(100, screen.get_height()))
        self.rect = self.image.get_rect(center = self.pos)
        self.dir = pygame.math.Vector2(self.pos).normalize()
        self.rect = self.image.get_rect(center = (round(self.pos.x),
                                                  round(self.pos.y)))
        self.timer = FPS * randint(1, 6)
        self.init_timer = self.timer // FPS

    def get_points(self):
        points = 1;
        if self.velocity > 8:
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
        self.__points -= count


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


def main():
    clock = pygame.time.Clock()
    finished = False
    player = Player("Test")#Player(input("Введите имя игрока: "))
    spawn_time = int(FPS*0.5)
    pygame.init()
    pygame.display.flip()
    balls = pygame.sprite.Group()
    balls.add(Ball(), Ball(), Ball())
    while not finished:
        clock.tick(FPS)
        balls.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for ball in balls:
                    if ball.mouse_in_ball(event):
                        print("CLICK")
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
    pygame.quit()
    print("Игрок", player.get_name(), "набрал очков: ", player.get_points())


if __name__ == "__main__":
    main()
