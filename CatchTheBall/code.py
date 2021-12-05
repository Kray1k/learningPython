#!/usr/bin/env python
# -*- coding: utf-8 -*

import pygame
from pygame.draw import *
from random import randint

FPS = 2
screen = pygame.display.set_mode((900, 600))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = (RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN)

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        self._screen = screen

    def new_ball(self):
        self.r = randint(30, 50)
        self.pos = pygame.math.Vector2(randint(100, 700), randint(100, 500))
        self.rect = self._screen.get_rect(center = self.pos)
        self.dir = pygame.math.Vector2(self.pos).normalize()
        self.color = COLORS[randint(0, 5)]
        circle(self._screen, self.color, self.pos, self.r)

    def reflect(self, NV):
        self.dir = self.dir.reflect(pygame.math.Vector2(NV))

    def update(self):
        self.pos += self.dir * 10
        self.rect.center = self.pos



    def mouse_in_ball(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        if (self.pos[0]-mouse_pos[0])**2 + \
                (self.pos[1]-mouse_pos[1])**2<= self.r**2:
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


def main():
    clock = pygame.time.Clock()
    finished = False
    #player = Player(input("Введите имя игрока: "))
    pygame.init()
    pygame.display.flip()
    ball = Ball(screen)
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ball.mouse_in_ball():
                    print("CLICK")
                    #player.add_points(1)
        ball.new_ball()
        pygame.display.flip()
        screen.fill(BLACK)
    pygame.quit()
    #print("Игрок", player.get_name(), "набрал", player.get_points(), "очка(ов)")


if __name__ == "__main__":
    main()
