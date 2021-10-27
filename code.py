#!/usr/bin/env python
# -*- coding: utf-8 -*
# How to blur effect:
# https://stackoverflow.com/questions/30723253/blurring-in-pygame

import pygame
from pygame.draw import *
from enum import Enum


screen = pygame.display.set_mode((800, 900))


class Color(Enum):
    LIGHT_GREY = 211, 211, 211
    DARK_GREY = 153, 153, 153
    DIM_GREY = 105, 105, 105
    BLACK_GREY = 51, 51, 51
    WHITE = 255, 255, 255
    OLIVE = 34, 43, 0
    DARK_BLUE = 0, 34, 43
    PALE_GOLDENROD= 238, 232, 170


def alien_ship(x: int, y: int, size: float = 1) -> None:
    """Рисует корабль пришельцев

    x, y - координаты, где отрисовывается корабль
    за х, у берется левый верхний угол корабля
    size - коэфицент размера корабля,
    рекомендованы значения [0, 2]
    """
    # Полупрозрачный квадрат света от тарелки
    # Создается новая поверхность surface - копия
    # текущего изображения на экране с новым форматом для
    # попиксельной обработки
    surface1 = screen.convert_alpha()
    # На surface1 рисуется треугольник белого цвета,
    # со смешиванием alpha 64 -> (64,) - [0, 255]
    polygon(surface1, Color.WHITE.value + (64,), [[x + 150*size, y], \
            [x + 300*size, y + 305*size], [x - size, y + 300*size]])
    # surface1 объединяется с основным изображением на экране
    screen.blit(surface1, (0, 0))
    # Рисуется корпус корабля - серая часть
    ellipse(screen, Color.DARK_GREY.value, (x, y, size*300, size*100))
    # Рисуется верх корабля - серо-светлая часть
    ellipse(screen, Color.LIGHT_GREY.value, (x + size*40, y - size*10, \
            size*220, size*80))
    # Рисуются белые эллипсы на корпусе корабля - 6 штук
    ellipse(screen, Color.WHITE.value, (x + 10*size, y + 40*size, \
            size*35, size*15))
    ellipse(screen, Color.WHITE.value, (x + 45*size, y + 65*size, \
            size*35, size*15))
    ellipse(screen, Color.WHITE.value, (x + 105*size, y + 75*size, \
            size*35, size*15))
    ellipse(screen, Color.WHITE.value, (x + 165*size, y + 75*size, \
            size*35, size*15))
    ellipse(screen, Color.WHITE.value, (x + 225*size, y + 65*size, \
            size*35, size*15))
    ellipse(screen, Color.WHITE.value, (x + 260*size, y + 40*size, \
            size*35, size*15))


def dim_grey_cloud(left, top) -> None:
    """Рисует облако серого цвета"""
    ellipse(screen, Color.DIM_GREY.value, (left, top, 800, 150))


def dark_grey_cloud(left: int, top: int) -> None:
    """Рисует облако темно-серого цвета"""
    ellipse(screen, Color.BLACK_GREY.value, (left, top, 800, 150))


def clouds() -> None:
    """Заполняет небо серыми и темно-серымы облаками."""
    dim_grey_cloud(550, -40)
    dim_grey_cloud(-250, 50)
    dim_grey_cloud(-400, 100)
    dim_grey_cloud(-350, 250)
    dim_grey_cloud(350, 150)
    dim_grey_cloud(300, 300)
    dark_grey_cloud(200, 100)
    dark_grey_cloud(-500, 200)
    dark_grey_cloud(250, 370)


def yellow_ellipse(left: int, top: int, h: int, w: int):
    ellipse(screen, Color.PALE_GOLDENROD.value, (left, top, h, w))


def alien(x: int, y: int, size: float = 1) -> None:
    yellow_ellipse(x+size, y+size, 20*size, 15*size)
    yellow_ellipse(x + 8*size, y + 15*size, 20*size, 10*size)

    arc(screen, Color.PALE_GOLDENROD.value, (x + 40*size, y + 60*size, \
            100*size, 200*size), 10, 6)


pygame.init()
window_size = pygame.display.get_window_size()
rect(screen, Color.OLIVE.value, (0, window_size[1]/2 + 100, \
        window_size[0], window_size[1]/2 - 100), width=0)
rect(screen, Color.DARK_BLUE.value, (0, 0, window_size[0], \
        window_size[1]/2 + 100))
line(screen, (46, 69, 68), (0, window_size[1]/2 + 100), (window_size[0], \
        window_size[1]/2 + 100))
circle(screen, Color.WHITE.value, (window_size[0] - window_size[0]/3, \
        window_size[1]/4), 120)



def main():
    clouds()
    alien_ship(100, 400)
    alien(100, 100)

    pygame.display.flip()
    try:
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == "q":
                    break
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
