import pygame

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
        text = pygame.font.SysFont("courier", 22, bold=True).render("Scramble", True, "black")
        text_rect = text.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text, text_rect)

    def draw(self, surf):
        surf.blit(self.surface, self.rect)
