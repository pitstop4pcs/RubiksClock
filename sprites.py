import pygame
import sys
import os


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Dial:
    def __init__(self, pos, idx, front=True):
        self.idx = idx
        self.surface = pygame.Surface((250, 250), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(center=pos)
        self.plus_surf = pygame.font.SysFont("courier",30, bold=True).render("+", True, "red")
        self.minus_surf = pygame.font.SysFont("courier", 30, bold=True).render("-", True, "red")
        self.minus_positions = [(self.surface.get_rect().left, self.surface.get_rect().y + 40),
                                (self.surface.get_rect().right - 60, self.surface.get_rect().y - 10),
                                (self.surface.get_rect().left + 50, self.surface.get_rect().bottom - 25),
                                (self.surface.get_rect().right - 15, self.surface.get_rect().bottom - 70)]
        self.plus_positions = [(self.surface.get_rect().left + 40, self.surface.get_rect().y - 10),
                                (self.surface.get_rect().right - 20, self.surface.get_rect().y + 30),
                                (self.surface.get_rect().left, self.surface.get_rect().bottom - 70),
                                (self.surface.get_rect().right - 60, self.surface.get_rect().bottom - 30)]
        self.r_minus_positions = [(self.surface.get_rect().right - 60, self.surface.get_rect().y - 10),
                                  (self.surface.get_rect().left, self.surface.get_rect().y + 40),
                                  (self.surface.get_rect().right - 15, self.surface.get_rect().bottom - 70),
                                  (self.surface.get_rect().left + 50, self.surface.get_rect().bottom - 25)]
        self.r_plus_positions = [(self.surface.get_rect().right - 20, self.surface.get_rect().y + 30),
                                 (self.surface.get_rect().left + 40, self.surface.get_rect().y - 10),
                                 (self.surface.get_rect().right - 60, self.surface.get_rect().bottom - 30),
                                 (self.surface.get_rect().left, self.surface.get_rect().bottom - 70)]
        self.minus_rect = self.minus_surf.get_rect(topleft=(self.minus_positions[self.idx]))
        self.r_minus_rect = self.minus_surf.get_rect(topleft=(self.r_minus_positions[self.idx]))
        self.plus_rect = self.plus_surf.get_rect(topleft=(self.plus_positions[self.idx]))
        self.r_plus_rect = self.plus_surf.get_rect(topleft=(self.r_plus_positions[self.idx]))
        if front:
            self.surface.blit(self.minus_surf, self.minus_rect)
            self.surface.blit(self.plus_surf, self.plus_rect)
        else:
            self.surface.blit(self.minus_surf, self.r_minus_rect)
            self.surface.blit(self.plus_surf, self.r_plus_rect)
        pygame.draw.circle(self.surface, "black", self.surface.get_rect().center, 125)

        self.nearest_clock = {0: 0,
                              1: 2,
                              2: 6,
                              3: 8}

        self.surrounding_clocks = {0: [0, 1, 3, 4],
                                   1: [1, 2, 4, 5],
                                   2: [3, 4, 6, 7],
                                   3: [4, 5, 7, 8]}

    def draw(self, surf):
        surf.blit(self.surface, self.rect)

    def minus(self, buttons_pressed, clock_faces):
        if buttons_pressed[self.idx]:
            for i, pressed in enumerate(buttons_pressed):
                if pressed:
                    clock_faces[self.nearest_clock[i]].time = (clock_faces[self.nearest_clock[i]].time - 1) % 12
        else:
            indices = []
            for i, pressed in enumerate(buttons_pressed):
                if not pressed:
                    for idx in self.surrounding_clocks[i]:
                        indices.append(idx)
            for idx in set(indices):
                clock_faces[idx].time = (clock_faces[idx].time - 1) % 12

    def plus(self, buttons_pressed, clock_faces):
        if buttons_pressed[self.idx]:
            for i, pressed in enumerate(buttons_pressed):
                if pressed:
                    clock_faces[self.nearest_clock[i]].time = (clock_faces[self.nearest_clock[i]].time + 1) % 12
        else:
            indices = []
            for i, pressed in enumerate(buttons_pressed):
                if not pressed:
                    for idx in self.surrounding_clocks[i]:
                        indices.append(idx)
            for idx in set(indices):
                clock_faces[idx].time = (clock_faces[idx].time + 1) % 12


class Button:
    def __init__(self, pos, idx, front=True):
        self.idx = idx
        self.surface = pygame.Surface((40, 40), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(center=pos)
        if front:
            self.pressed = False
        else:
            self.pressed = True

    def press(self):
        if self.pressed:
            self.pressed = False
        else:
            self.pressed = True

    def draw(self, surf):
        if self.pressed:
            pygame.draw.circle(self.surface, "black", self.surface.get_rect().center, 20)
        else:
            pygame.draw.circle(self.surface, "white", self.surface.get_rect().center, 20)
            pygame.draw.circle(self.surface, "black", self.surface.get_rect().center, 20, 1)
        surf.blit(self.surface, self.rect)


class ClockFace:
    def __init__(self, pos, idx, front=True):
        self.front = front
        self.idx = idx
        self.time = 0
        self.surface = pygame.Surface((180, 180), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(center=pos)
        self.hand_startpoint = pygame.math.Vector2(self.surface.get_rect().center)
        self.hand_endpoint = pygame.math.Vector2(0, -70)

    def draw(self, surf):
        self.surface.fill(pygame.SRCALPHA)
        if self.front:
            pygame.draw.circle(self.surface, "white", (90, 90), 75)
        else:
            pygame.draw.circle(self.surface, "cyan", (90, 90), 75)
        pygame.draw.circle(self.surface, "black", (90, 90), 75, 2)
        pygame.draw.circle(self.surface, "red", (self.surface.get_rect().centerx, self.surface.get_rect().top + 5), 5, 0)
        pygame.draw.line(self.surface, "black", self.hand_startpoint,
                         self.hand_startpoint + self.hand_endpoint.rotate(self.time * 30), 4)
        surf.blit(self.surface, self.rect)


class ResetButton:
    def __init__(self, pos):
        self.surface = pygame.Surface((120, 50), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(center=pos)
        pygame.draw.rect(self.surface, "white", (0, 0, 120, 50), 0, 8)
        pygame.draw.rect(self.surface, "black", (0, 0, 120, 50), 1, 8)
        text = pygame.font.SysFont("courier", 22, bold=True).render("Reset", True, "black")
        text_rect = text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text, text_rect)

    def draw(self, surf):
        surf.blit(self.surface, self.rect)


class ScrambleButton:
    def __init__(self, pos):
        self.surface = pygame.Surface((120, 50), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(center=pos)
        pygame.draw.rect(self.surface, "white", (0, 0, 120, 50), 0, 8)
        pygame.draw.rect(self.surface, "black", (0, 0, 120, 50), 1, 8)
        text = pygame.font.SysFont("courier", 22, bold=True).render("Start", True, "black")
        text_rect = text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text, text_rect)

    def draw(self, surf):
        surf.blit(self.surface, self.rect)


class KeyboardGraphic:
    def __init__(self, key, pos):
        if key == "return":
            self.surface = pygame.Surface((80, 80), pygame.SRCALPHA, 32).convert_alpha()
            self.rect = self.surface.get_rect(center=pos)
            pygame.draw.rect(self.surface, "white", (0, 0, 80, 40), 0, 6, 6, 6, 6, 0)
            pygame.draw.rect(self.surface, "white", (18, 40, 62, 40), 0, 6, 0, 0, 6, 6)
            pygame.draw.rect(self.surface, "black", (0, 0, 80, 40), 2, 6, 6, 6, 6, 0)
            pygame.draw.rect(self.surface, "black", (18, 40, 62, 40), 2, 6, 0, 0, 6, 6)
            pygame.draw.rect(self.surface, "black", (4, 4, 72, 32), 2, 6, 6, 6, 6, 0)
            pygame.draw.rect(self.surface, "black", (22, 44, 54, 32), 2, 6, 0, 0, 6, 6)
            pygame.draw.rect(self.surface, "white", (20, 34, 58, 12))
            pygame.draw.line(self.surface, "black", (22, 34), (22, 56), 2)
            pygame.draw.line(self.surface, "black", (20, 34), (22, 34), 2)
            pygame.draw.line(self.surface, "black", (74, 34), (74, 45), 2)
            pygame.draw.line(self.surface, "black", (15, 23), (40, 23), 3)
            pygame.draw.line(self.surface, "black", (40, 23), (40, 12), 3)
            pygame.draw.polygon(self.surface, "black", [(15, 23), (20, 20), (20, 26)], 0)
        elif key == "space":
            self.surface = pygame.Surface((160, 40), pygame.SRCALPHA, 32).convert_alpha()
            self.rect = self.surface.get_rect(center=pos)
            pygame.draw.rect(self.surface, "white", (0, 0, 160, 40), 0, 6)
            pygame.draw.rect(self.surface, "black", (0, 0, 160, 40), 2, 6)
            pygame.draw.rect(self.surface, "black", (4, 4, 152, 32), 1, 8)
            pygame.draw.line(self.surface, "black", (50,28), (110, 28), 2)
            pygame.draw.line(self.surface, "black", (50,28), (50, 15), 2)
            pygame.draw.line(self.surface, "black", (110,28), (110, 15), 2)
        elif key == "shift":
            self.surface = pygame.Surface((60, 40), pygame.SRCALPHA, 32).convert_alpha()
            self.rect = self.surface.get_rect(center=pos)
            pygame.draw.rect(self.surface, "white", (0, 0, 60, 40), 0, 6)
            pygame.draw.rect(self.surface, "black", (0, 0, 60, 40), 2, 6)
            pygame.draw.rect(self.surface, "black", (4, 4, 52, 32), 1, 8)
            img = pygame.image.load(resource_path("shift.png")).convert_alpha()
            img_rect = img.get_rect(topleft=(0, 4))
            self.surface.blit(img, img_rect)
        elif key == "esc":
            self.surface = pygame.Surface((40, 35), pygame.SRCALPHA, 32).convert_alpha()
            self.rect = self.surface.get_rect(center=pos)
            pygame.draw.rect(self.surface, "white", (0, 0, 40, 35), 0, 6)
            pygame.draw.rect(self.surface, "black", (0, 0, 40, 35), 2, 6)
            pygame.draw.rect(self.surface, "black", (4, 4, 32, 27), 1, 8)
            text = pygame.font.SysFont("courier", 14, bold=True).render("Esc", True, "black")
            text_rect = text.get_rect(topleft=(6, 6))
            self.surface.blit(text, text_rect)
        else:
            self.surface = pygame.Surface((40, 40), pygame.SRCALPHA, 32).convert_alpha()
            self.rect = self.surface.get_rect(center=pos)
            pygame.draw.rect(self.surface, "white", (0, 0, 40, 40), 0, 6)
            pygame.draw.rect(self.surface, "black", (0, 0, 40, 40), 2, 6)
            pygame.draw.rect(self.surface, "black", (4, 4, 32, 32), 1, 8)
            text = pygame.font.SysFont("courier", 30, bold=True).render(key.upper(), True, "black")
            text_rect = text.get_rect(topleft=(5, 0))
            self.surface.blit(text, text_rect)

    def draw(self, surf):
        surf.blit(self.surface, self.rect)


class FlipButton:
    def __init__(self, pos, front=True):
        if front:
            self.surface = pygame.image.load(resource_path("flip.png")).convert_alpha()
        else:
            self.surface = pygame.transform.flip(pygame.image.load(resource_path("flip.png")).convert_alpha(), True, False)
        self.rect = self.surface.get_rect(center=pos)

    def draw(self, surf):
        surf.blit(self.surface, self.rect)
