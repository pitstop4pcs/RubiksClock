import random
import pygame

from sprites import resource_path, ClockFace, Button, Dial, ResetButton, ScrambleButton, KeyboardGraphic, FlipButton


class Game:
    def __init__(self):
        clock_positions = [(200, 200), (400, 200), (600, 200),
                           (200, 400), (400, 400), (600, 400),
                           (200, 600), (400, 600), (600, 600)]
        r_clock_positions = [(600, 200), (400, 200), (200, 200),
                           (600, 400), (400, 400), (200, 400),
                           (600, 600), (400, 600), (200, 600)]
        button_positions = [(300, 300), (500, 300), (300, 500), (500, 500)]
        r_button_positions = [(500, 300), (300, 300), (500, 500), (300, 500)]
        dial_positions = [(200, 200), (600, 200), (200, 600), (600, 600)]
        r_dial_positions = [(600, 200), (200, 200), (600, 600), (200, 600)]
        pygame.init()
        pygame.display.set_caption("Rubik's Clock")
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_icon(pygame.image.load(resource_path("rubik.ico")).convert_alpha())
        self.running = True
        self.game_started = False
        self.solved = False
        self.game_clock = pygame.time.Clock()
        self.front = True

        self.clock_faces = [ClockFace(pos, i) for i, pos in enumerate(clock_positions)]
        self.buttons = [Button(pos, i) for i, pos in enumerate(button_positions)]
        self.dials = [Dial(pos, i) for i, pos in enumerate(dial_positions)]

        self.r_clock_faces = [ClockFace(pos, i, False) for i, pos in enumerate(r_clock_positions)]
        self.r_buttons = [Button(pos, i, False) for i, pos in enumerate(r_button_positions)]
        self.r_dials = [Dial(pos, i, False) for i, pos in enumerate(r_dial_positions)]

        self.reset_button = ResetButton((330, 715))
        self.scramble_button = ScrambleButton((470, 715))

        self.front_flip_button = FlipButton((self.screen.get_rect().centerx, 80))
        self.rear_flip_button = FlipButton((self.screen.get_rect().centerx, 80), False)

        self.timer = 0
        try:
            with open(resource_path("best.txt"), "r") as file:
                self.best = float(file.read())
        except Exception as e:
            print(e)
            self.best: float = 0
            with open(resource_path("best.txt"), "w") as file:
                file.write(str(self.best))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse_click(event.pos)
                    elif event.button == 3:
                        self.flip()
                if event.type == pygame.KEYDOWN:
                    self.key_press(pygame.key.get_pressed())

            if self.game_started:
                if set(cf.time for cf in [*self.clock_faces, *self.r_clock_faces]) == {0}:
                    self.completed()
                else:
                    self.timer += 1/60
            self.game_clock.tick(60)
            self.display_update()
        pygame.quit()

    def flip(self):
        if self.front:
            self.front = False
        else:
            self.front = True

    def key_press(self, keys):
        if keys[pygame.K_SPACE]:
            self.flip()
        if keys[pygame.K_ESCAPE]:
            self.reset()
        if keys[pygame.K_RETURN]:
            self.scramble()
        if not self.solved:
            if self.front:
                if keys[pygame.K_q]:
                    self.buttons[0].press()
                    self.r_buttons[0].press()
                if keys[pygame.K_w]:
                    self.buttons[1].press()
                    self.r_buttons[1].press()
                if keys[pygame.K_a]:
                    self.buttons[2].press()
                    self.r_buttons[2].press()
                if keys[pygame.K_s]:
                    self.buttons[3].press()
                    self.r_buttons[3].press()

                if keys[pygame.K_i]:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.dials[0].minus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[0].plus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
                    else:
                        self.dials[0].plus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[0].minus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)

                if keys[pygame.K_o]:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.dials[1].minus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[1].plus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
                    else:
                        self.dials[1].plus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[1].minus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)

                if keys[pygame.K_k]:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.dials[2].minus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[2].plus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
                    else:
                        self.dials[2].plus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[2].minus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)

                if keys[pygame.K_l]:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.dials[3].minus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[3].plus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
                    else:
                        self.dials[3].plus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[3].minus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
            else:
                if keys[pygame.K_q]:
                    self.buttons[1].press()
                    self.r_buttons[1].press()
                if keys[pygame.K_w]:
                    self.buttons[0].press()
                    self.r_buttons[0].press()
                if keys[pygame.K_a]:
                    self.buttons[3].press()
                    self.r_buttons[3].press()
                if keys[pygame.K_s]:
                    self.buttons[2].press()
                    self.r_buttons[2].press()

                if keys[pygame.K_i]:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.dials[1].plus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[1].minus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
                    else:
                        self.dials[1].minus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[1].plus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)

                if keys[pygame.K_o]:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.dials[0].plus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[0].minus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
                    else:
                        self.dials[0].minus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[0].plus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)


                if keys[pygame.K_k]:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.dials[3].plus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[3].minus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
                    else:
                        self.dials[3].minus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[3].plus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)


                if keys[pygame.K_l]:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.dials[2].plus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[2].minus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
                    else:
                        self.dials[2].minus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[2].plus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)


    def completed(self):
        self.solved = True
        if self.timer < self.best or self.best == 0:
            self.best = self.timer
            with open(resource_path("best.txt"), "w") as file:
                file.write(str(self.best))

    def mouse_click(self, pos):
        if self.front:
            if self.front_flip_button.rect.collidepoint(pos):
                self.flip()
            if self.reset_button.rect.collidepoint(pos):
                self.reset()
            if self.scramble_button.rect.collidepoint(pos):
                self.scramble()
            if not self.solved:
                for i, button in enumerate(self.buttons):
                    if button.rect.collidepoint(pos):
                        button.press()
                        self.r_buttons[i].press()
                for i, dial in enumerate(self.dials):
                    if pygame.rect.Rect(dial.minus_rect.x + dial.rect.x, dial.minus_rect.y + dial.rect.y, 50,
                                        50).collidepoint(pos):
                        dial.minus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[i].plus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
                    if pygame.rect.Rect(dial.plus_rect.x + dial.rect.x, dial.plus_rect.y + dial.rect.y, 50,
                                        50).collidepoint(pos):
                        dial.plus([button.pressed for button in self.buttons], self.clock_faces)
                        self.r_dials[i].minus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
        else:
            if self.rear_flip_button.rect.collidepoint(pos):
                self.flip()
            if not self.solved:
                for i, r_button in enumerate(self.r_buttons):
                    if r_button.rect.collidepoint(pos):
                        r_button.press()
                        self.buttons[i].press()
                for i, r_dial in enumerate(self.r_dials):
                    if pygame.rect.Rect(r_dial.r_minus_rect.x + r_dial.rect.x, r_dial.r_minus_rect.y + r_dial.rect.y, 50,
                                        50).collidepoint(pos):
                        r_dial.minus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
                        self.dials[i].plus([button.pressed for button in self.buttons], self.clock_faces)
                    if pygame.rect.Rect(r_dial.r_plus_rect.x + r_dial.rect.x, r_dial.r_plus_rect.y + r_dial.rect.y, 50,
                                        50).collidepoint(pos):
                        r_dial.plus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
                        self.dials[i].minus([button.pressed for button in self.buttons], self.clock_faces)

    def reset(self):
        for clock_face in [*self.clock_faces, *self.r_clock_faces]:
            clock_face.time = 0
        for button in self.buttons:
            button.pressed = False
        for r_button in self.r_buttons:
            r_button.pressed = True
        self.game_started = False
        self.timer = 0

    def scramble(self):
        for _ in range(100):
            n = random.randint(0, 3)
            self.buttons[n].press()
            self.r_buttons[n].press()
            n = random.randint(0, 3)
            self.dials[n].plus([button.pressed for button in self.buttons], self.clock_faces)
            self.r_dials[n].minus([r_button.pressed for r_button in self.r_buttons], self.r_clock_faces)
        self.timer = 0
        self.solved = False
        self.game_started = True

    def display_update(self):
        self.screen.fill("skyblue3")
        if self.front:
            [dial.draw(self.screen) for dial in self.dials]
            pygame.draw.circle(self.screen, "cyan", (400, 400), 375)
            pygame.draw.circle(self.screen, "black", (400, 400), 375, 5)
            [clock_face.draw(self.screen) for clock_face in self.clock_faces]
            [button.draw(self.screen) for button in self.buttons]
            front = pygame.font.SysFont("courier", 30, bold=True).render("Front", True, "black")
            front_rect = front.get_rect(center=(self.screen.get_rect().centerx, 50))
            self.screen.blit(front, front_rect)
            self.reset_button.draw(self.screen)
            self.scramble_button.draw(self.screen)
            self.front_flip_button.draw(self.screen)
        else:
            [r_dial.draw(self.screen) for r_dial in self.r_dials]
            pygame.draw.circle(self.screen, "white", (400, 400), 375)
            pygame.draw.circle(self.screen, "black", (400, 400), 375, 5)
            [r_clock_face.draw(self.screen) for r_clock_face in self.r_clock_faces]
            [r_button.draw(self.screen) for r_button in self.r_buttons]
            back = pygame.font.SysFont("courier", 30, bold=True).render("Back", True, "black")
            back_rect = back.get_rect(center=(self.screen.get_rect().centerx, 50))
            self.screen.blit(back, back_rect)
            self.rear_flip_button.draw(self.screen)

        time = round(self.timer * 100)
        secs, huns = divmod(time, 100)
        mins, secs = divmod(secs, 60)
        hrs, mins = divmod(mins, 60)
        huns = str("%02d" % round(huns),)
        secs = str("%02d" % round(secs),)
        mins = str("%02d" % (round(mins),))
        hrs = str(round(hrs))
        colour = "red" if self.solved else "black"
        timer = pygame.font.SysFont("courier", 30, bold=True).render(f"{hrs}:{mins}:{secs}.{huns}", True, colour)
        timer_rect = timer.get_rect(topleft=(self.screen.get_rect().right - 180, self.screen.get_rect().top))
        self.screen.blit(timer, timer_rect)

        time = round(self.best * 100)
        secs, huns = divmod(time, 100)
        mins, secs = divmod(secs, 60)
        hrs, mins = divmod(mins, 60)
        huns = str("%02d" % round(huns),)
        secs = str("%02d" % round(secs),)
        mins = str("%02d" % (round(mins),))
        hrs = str(round(hrs))
        timer = pygame.font.SysFont("courier", 30, bold=True).render(f"{hrs}:{mins}:{secs}.{huns}", True, "black")
        timer_rect = timer.get_rect(topleft=(self.screen.get_rect().left, self.screen.get_rect().top))
        self.screen.blit(timer, timer_rect)

        if not self.game_started:
            KeyboardGraphic("q", (280, 280)).draw(self.screen)
            KeyboardGraphic("w", (520, 280)).draw(self.screen)
            KeyboardGraphic("a", (280, 480)).draw(self.screen)
            KeyboardGraphic("s", (520, 480)).draw(self.screen)
            KeyboardGraphic("i", (90, 55)).draw(self.screen)
            KeyboardGraphic("o", (750, 145)).draw(self.screen)
            KeyboardGraphic("k", (50, 650)).draw(self.screen)
            KeyboardGraphic("l", (710, 735)).draw(self.screen)
            KeyboardGraphic("shift", (32, 162)).draw(self.screen)
            KeyboardGraphic("i", (84, 162)).draw(self.screen)
            KeyboardGraphic("shift", (720, 55)).draw(self.screen)
            KeyboardGraphic("o", (772, 55)).draw(self.screen)
            KeyboardGraphic("shift", (50, 745)).draw(self.screen)
            KeyboardGraphic("k", (102, 745)).draw(self.screen)
            KeyboardGraphic("shift", (726, 640)).draw(self.screen)
            KeyboardGraphic("l", (778, 640)).draw(self.screen)
            KeyboardGraphic("space", (500, 100)).draw(self.screen)
            if self.front:
                KeyboardGraphic("return", (555, 755)).draw(self.screen)
                KeyboardGraphic("esc", (270, 745)).draw(self.screen)

        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
