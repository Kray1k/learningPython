#!/usr/bin/env python
# -*- coding: utf-8 -*

import pygame
from pygame.draw import *
from enum import Enum
from PIL import Image, ImageFilter
from os import remove
from time import sleep


screen = pygame.display.set_mode((800, 900))
window_size = pygame.display.get_window_size()


class Color(Enum):
    LIGHT_GREY = 211, 211, 211
    DARK_GREY = 153, 153, 153
    DIM_GREY = 105, 105, 105
    BLACK_GREY = 51, 51, 51
    WHITE = 255, 255, 255
    OLIVE = 34, 43, 0
    DARK_BLUE = 0, 34, 43
    PALE_GOLDENROD= 238, 232, 170
    BLACK = 0, 0, 0
    RED = 200, 55, 55
    GREEN = 136, 170, 0


def alien_ship(x: int, y: int, size: float = 1) -> None:
    """Рисует корабль пришельцев

    x, y - координаты, где отрисовывается корабль
    за х, у берется левый верхний угол корабля
    size - коэфицент размера корабля,
    рекомендованы значения [0, 2]
    """
    #TODO: Создать отдельную поверхность для рисунка, и масштабировать его
    # через pygame.transform.smoothscale(surface, (width, height))
    # вместо расчета размера каждого элемента рисунка
    #
    # Полупрозрачный треугольник света от тарелки
    # Создается новая поверхность surface - копия
    # текущего изображения на экране с новым форматом для
    # попиксельной обработки
    surface1 = screen.convert_alpha()
    # На surface1 рисуется треугольник белого цвета,
    # со смешиванием alpha 64 -> (64,) - [0, 255]
    polygon(surface1, Color.WHITE.value + (64,), [[x + 150*size, y],
            [x + 300*size, y + 305*size], [x - size, y + 300*size]])
    # surface1 объединяется с основным изображением на экране
    screen.blit(surface1, (0, 0))
    # Рисуется корпус корабля - серая часть
    ellipse(screen, Color.DARK_GREY.value, (x, y, size*300, size*100))
    # Рисуется верх корабля - серо-светлая часть
    ellipse(screen, Color.LIGHT_GREY.value, (x + size*40, y - size*10,
            size*220, size*80))
    # Рисуются белые эллипсы на корпусе корабля - 6 штук
    ellipse(screen, Color.WHITE.value, (x + 10*size, y + 40*size, size*35,
                                        size*15))
    ellipse(screen, Color.WHITE.value, (x + 45*size, y + 65*size, size*35,
                                        size*15))
    ellipse(screen, Color.WHITE.value, (x + 105*size, y + 75*size, size*35,
                                        size*15))
    ellipse(screen, Color.WHITE.value, (x + 165*size, y + 75*size, size*35,
                                        size*15))
    ellipse(screen, Color.WHITE.value, (x + 225*size, y + 65*size, size*35,
                                        size*15))
    ellipse(screen, Color.WHITE.value, (x + 260*size, y + 40*size, size*35,
                                        size*15))


def dim_grey_cloud(left, top) -> None:
    """Рисует облако серого цвета"""
    surface0 = pygame.Surface((window_size[0], window_size[1]), pygame.SRCALPHA)
    ellipse(surface0, Color.DIM_GREY.value, (left, top, 800, 150))
    pygame.image.save(surface0, "aga.png")
    sleep(0.1)
    blured = Image.open("aga.png").filter(ImageFilter.GaussianBlur(radius=50))
    surface0 = pygame.image.fromstring(blured.tobytes(), (window_size[0],
                                                          window_size[1]),
                                       blured.mode)
    screen.blit(surface0, (0, 0))


def dark_grey_cloud(left: int, top: int) -> None:
    """Рисует облако темно-серого цвета"""
    surface0 = pygame.Surface((window_size[0], window_size[1]), pygame.SRCALPHA)
    ellipse(surface0, Color.DARK_GREY.value, (left, top, 800, 150))
    pygame.image.save(surface0, "aga.png")
    sleep(0.1)
    blured = Image.open("aga.png").filter(ImageFilter.GaussianBlur(radius=50))
    surface0 = pygame.image.fromstring(blured.tobytes(), (window_size[0],
                                                          window_size[1]),
                                       blured.mode)
    screen.blit(surface0, (0, 0))

def clouds() -> None:
    """Заполняет небо серыми и темно-серымы облаками."""
    # TODO: в функциях dim_grey_cloud и dark_grey_cloud произвести оптимизацию
    # (повторяющийся код) и найти способ буферного хранения Image в строке
    # а не в файле aga.png
    dim_grey_cloud(550, -40)
    dim_grey_cloud(-250, 50)
    dim_grey_cloud(-400, 100)
    dim_grey_cloud(-350, 250)
    dim_grey_cloud(350, 150)
    dim_grey_cloud(300, 300)
    dark_grey_cloud(200, 100)
    dark_grey_cloud(-500, 200)
    dark_grey_cloud(250, 370)
    remove("aga.png")


def yellow_ellipse(surface0, left: int, top: int, w: int, h: int) -> None:
    ellipse(surface0, Color.PALE_GOLDENROD.value, (left, top, w, h))


def ellipse_on_surface(surface0, left: int, top: int, w: int, h: int,
                       sW:int, sH: int,
                       angle: int = 0, width: int = 0,
                       color = Color.PALE_GOLDENROD.value) -> None:
    """Рисует обрезанный или повернутый эллипс желтого цвета
    left, top - позиция на итоговом рисунке
    w, h - ширина и высота эллипса
    Эллпис обрезается прямоугольником area с параметрами sW, sH:
        sW, Sh - ширина и высота прямоугольника
    Эллипс выводится без изменений если параметры прямоугольника совпадают с
    параметрами эллписа
    angle - угол поворота обрезанного (или нет) эллписа
    width - вместо эллипса рисует обводку черного цвета если не 0
    color - цвет эллипса, по умолчанию желтый
    """
    surface1 = pygame.Surface((w, h),
                              pygame.SRCALPHA)
    if width == 0:
        ellipse(surface1, color, (0, 0, w, h))
    else:
        ellipse(surface1, Color.BLACK.value, (0, 0, w, h), width)
    if angle != 0:
        surface2 = pygame.Surface((w, h),
                                  pygame.SRCALPHA)
        surface2.blit(surface1, (0, 0), (0, 0, sW, sH)) 
        surface2 = pygame.transform.rotate(surface2, angle)
        surface0.blit(surface2, (left, top))
    else:
        surface0.blit(surface1, (left, top), (0, 0, sW, sH))


def alien(x: int, y: int, size: float = 1, revers: bool = 0) -> None:
    """Рисует пришельца
    х, у - координаты левого верхнего угла пришельца (left, top)
    size - коэфицент размера
    revers - отражение по горизонтали (bool - ноль или не ноль)
    """
    surface0 = pygame.Surface((200, 300), pygame.SRCALPHA)
    # Туловище
    yellow_ellipse(surface0, 40, 120, 45, 100)
    # Левое ухо
    yellow_ellipse(surface0, 0, 0, 25, 20)
    yellow_ellipse(surface0, 5, 18, 20, 10)
    yellow_ellipse(surface0, 15, 30, 15, 18)
    yellow_ellipse(surface0, 25, 45, 10, 15)
    # Левая часть головы
    ellipse_on_surface(surface0, 10, 50, 80, 40, 80, 40, 120)
    ellipse_on_surface(surface0, 10, 50, 80, 40, 80, 25, 120, 2)
    ellipse_on_surface(surface0, 12, 50, 80, 40, 20, 40, 220, 2)
    # Правая часть головы
    ellipse_on_surface(surface0, 45, 53, 80, 40, 80, 40, 50)
    ellipse_on_surface(surface0, 45, 53, 80, 40, 80, 16, 230, 2)
    # Верхняя часть головы
    ellipse_on_surface(surface0, 23,  55, 100, 40, 90, 40, 2)
    # "Волосок" на левой части головы
    ellipse_on_surface(surface0, 15, 15, 80, 40, 20, 20, 80, 2)
    # Правое ухо
    yellow_ellipse(surface0, 100, 50, 15, 15)
    yellow_ellipse(surface0, 105, 40, 10, 15)
    yellow_ellipse(surface0, 110, 25, 15, 15)
    yellow_ellipse(surface0, 125, 20, 15, 10)
    yellow_ellipse(surface0, 140, 25, 20, 25)
    # Левый глаз
    circle(surface0, Color.BLACK.value, (50, 85), 15)
    circle(surface0, Color.WHITE.value, (55, 88), 3)
    # Правый глаз
    circle(surface0, Color.BLACK.value, (90, 90), 10)
    circle(surface0, Color.WHITE.value, (93, 93), 3)
    # Левая рука
    yellow_ellipse(surface0, 25, 130, 25, 25)
    yellow_ellipse(surface0, 15, 145, 20, 15)
    yellow_ellipse(surface0, 5, 160, 10, 15)
    # Правая рука
    yellow_ellipse(surface0, 80, 135, 25, 25)
    yellow_ellipse(surface0, 95, 145, 22, 17)
    yellow_ellipse(surface0, 120, 150, 28, 15)
    # Яблоко
    circle(surface0, Color.RED.value, (160, 135), 25)
    arc(surface0, Color.BLACK.value, (160, 100, 30, 40), 8, 9.3, 2)
    ellipse_on_surface(surface0, 165, 90, 2, 8, 2, 8, 20,
                       color = Color.GREEN.value)
    # Левая нога
    yellow_ellipse(surface0, 30, 190, 25, 40)
    yellow_ellipse(surface0, 25, 220, 20, 50)
    yellow_ellipse(surface0, 10, 255, 20, 20)
    # Правая нога
    yellow_ellipse(surface0, 70, 200, 25, 40)
    yellow_ellipse(surface0, 75, 230, 20, 50)
    yellow_ellipse(surface0, 90, 265, 20, 20)
    if size != 1:
        surface0 = pygame.transform.smoothscale(surface0, (200 * size,
                                                           300 * size))
    if revers:
        surface0 = pygame.transform.flip(surface0, 1, 0)
    screen.blit(surface0, (x, y))


def main() -> None:
    pygame.init()
    #TODO: Вместо фигур сделать заливку поверхности screen через fill
    rect(screen, Color.OLIVE.value,
         (0, window_size[1]/2 + 100, window_size[0], window_size[1]/2 - 100),
         width=0)
    rect(screen, Color.DARK_BLUE.value, (0, 0, window_size[0],
                                         window_size[1]/2 + 100))
    line(screen, (46, 69, 68), (0, window_size[1]/2 + 100),
        (window_size[0], window_size[1]/2 + 100))
    circle(screen, Color.WHITE.value,
           (window_size[0] - window_size[0]/3, window_size[1]/4), 120)
    clouds()
    alien(150, 500, 0.5, 1)
    alien_ship(100, 400)
    alien_ship(200, 400)
    alien(500, 500, 1, 0)
    alien_ship(350, 500, 0.2)
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
