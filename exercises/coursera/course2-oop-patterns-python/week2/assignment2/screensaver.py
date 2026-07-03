#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import math
import pygame
import random
from typing import List, Tuple

SCREEN_DIM = (800, 600)


class Vec2d:
    """Двумерный вектор и его методы.

    Вектор определяется координатами x, y — точка конца вектора.
    Начало вектора всегда совпадает с центом координат (0, 0).
    """

    def __init__(self, x: float, y: float):
        """Инициализирует объект двумерного вектора.

        Args:
            x (int): координата точки конца вектора на оси X
            y (int): координата точки конца вектора на оси Y
        """
        self.x = x
        self.y = y

    def __add__(self, other: Vec2d) -> Vec2d:
        """Сумма двух векторов.

        Args:
            other (Vec2d): другой вектор

        Returns:
            Vec2d: новый вектор
        """
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2d) -> Vec2d:
        """Разность двух векторов.

        Args:
            other (Vec2d): другой вектор

        Returns:
            Vec2d: новый вектор
        """
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, k: int) -> Vec2d:
        """Произведение вектора на число.

        Args:
            k (int): число

        Returns:
            Vec2d: новый вектор
        """
        return Vec2d(self.x * k, self.y * k)

    def __len__(self) -> Vec2d:
        """Длина вектора.

        Returns:
            Vec2d: новый вектор
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self) -> Tuple[int, int]:
        """Текущие координаты вектора.

        Returns:
            Tuple[int, int]
        """
        return int(self.x), int(self.y)


class Polyline:
    """Класс замкнутых ломаных."""

    def __init__(self, game_display, points: List[Vec2d] = None):
        self.game_display = game_display
        self.points = [] if not points else points
        self.speeds = []

    def clear(self):
        self.points = []
        self.speeds = []

    def set_points(self):
        """Перерасчет координат опорных точек."""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]

            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)

            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, style: str = "points", width: int = 3, color: Tuple = (255, 255, 255)):
        """Отрисовка точек на экране."""
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(self.game_display, color,
                                 self.points[p_n].int_pair(),
                                 self.points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(self.game_display, color,
                                   p.int_pair(), width)


class Knot(Polyline):
    def __init__(self, game_display, steps: int, points: List[Vec2d] = None):
        super().__init__(game_display, points=points)
        self.steps = steps

    def draw_points(self, style: str = "line", width: int = 3, color: Tuple = (255, 255, 255)):
        """Отрисовка точек на экране."""
        self.points = self._get_knot()
        super().draw_points(style=style, width=width, color=color)

    def _get_knot(self):
        """Расчет точек кривой по добавляемым «опорным» точкам."""
        if len(self.points) < 3:
            return []

        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self._get_points(ptn, self.steps))
        return res

    def _get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self._get_point(base_points, i * alpha))
        return res

    def _get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self._get_point(points, alpha, deg - 1) * (1 - alpha)


class ScreenSaver:
    def __init__(self, caption="MyScreenSaver"):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption(caption)

        self.steps = 35
        self.working = True
        self.show_help = False
        self.pause = True

        self.polyline = Polyline(self.gameDisplay)

        self.hue = 0
        self.color = pygame.Color(0)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._quit()
                if event.key == pygame.K_r:
                    self.polyline.clear()
                if event.key == pygame.K_p:
                    self._pause()
                if event.key == pygame.K_KP_PLUS:
                    self._inc_steps()
                if event.key == pygame.K_F1:
                    self._show_help()
                if event.key == pygame.K_KP_MINUS:
                    self._dec_steps()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.polyline.points.append(Vec2d(*event.pos))
                self.polyline.speeds.append(
                    Vec2d(random.random() * 2, random.random() * 2))

    def _quit(self):
        self.working = False

    def _pause(self):
        self.pause = not self.pause

    def _show_help(self):
        self.show_help = not self.show_help

    def _inc_steps(self):
        self.steps += 1

    def _dec_steps(self):
        self.steps -= 1 if self.steps > 1 else 0

    def _draw_help(self):
        """Отрисовка справки программы."""
        self.gameDisplay.fill((50, 50, 50))

        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)

        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def _update_colors(self):
        self.gameDisplay.fill((0, 0, 0))
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)

    def display(self):
        while self.working:
            self._handle_events()
            self._update_colors()

            self.polyline.draw_points()

            knot = Knot(self.gameDisplay, self.steps, self.polyline.points)
            knot.draw_points(color=self.color)

            if not self.pause:
                self.polyline.set_points()

            if self.show_help:
                self._draw_help()

            pygame.display.flip()

        self.exit()

    @staticmethod
    def exit():
        pygame.display.quit()
        pygame.quit()
        exit(0)


if __name__ == "__main__":
    screensaver = ScreenSaver()
    screensaver.display()
