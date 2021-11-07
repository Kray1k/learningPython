#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.draw import *
from enum import Enum

screen = pygame.display.set_mode((800, 600))
window_size = pygame.display.get_window_size()
smile_size = int()


class Color(Enum):
    YELLOW = 255, 255, 0
    BLACK = 0, 0, 0
    RED = 255, 0, 0


def head(surface) -> None:
    r = smile_size / 2
    circle(surface, Color.YELLOW.value, (smile_size/2, smile_size/2), r)
    circle(surface, Color.YELLOW.value, (smile_size/2, smile_size/2), r, 2)


def eyes(surface) -> None:
    r = smile_size / 12
    #left
    circle(surface, Color.RED.value, (smile_size/4,
                                     smile_size/4 + smile_size/8), r)
    circle(surface, Color.BLACK.value, (smile_size/4,
                                     smile_size/4 + smile_size/8), r, 2)
    circle(surface, Color.BLACK.value, (smile_size/4,
                                     smile_size/4 + smile_size/8), r/2.5)
    # right
    circle(surface, Color.RED.value, (smile_size/4 + smile_size/2,
                                     smile_size/4 + smile_size/8), r/1.2)
    circle(surface, Color.BLACK.value, (smile_size/4 + smile_size/2,
                                     smile_size/4 + smile_size/8), r/1.2, 2)
    circle(surface, Color.BLACK.value, (smile_size/4 + smile_size/2,
                                     smile_size/4 + smile_size/8), r/2.5)


def mouth(surface) -> None:
    x = smile_size/4
    y = smile_size - smile_size/4
    w = smile_size/2
    h = smile_size/10
    rect(surface, Color.BLACK.value, (x, y, w, h))


def calculate_xy() -> tuple:
    global smile_size
    if window_size[0] > window_size[1]:
        smile_size = window_size[1]
        return ((window_size[0] - smile_size) / 2 , 0)
    elif window_size[0] < window_size[1]:
        smile_size = window_size[0]
        return (0, (window_size[1] - smile_size) / 2)
    smile_size = window_size[0]
    return (0, 0)


def angry_smile() -> None:
    xy = calculate_xy()
    surface = pygame.Surface((window_size[0], window_size[1]),
                             pygame.SRCALPHA)
    head(surface)
    mouth(surface)
    eyes(surface)
    screen.blit(surface, xy)


def main():
    pygame.init()
    angry_smile()

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
