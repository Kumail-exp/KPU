#i am bad with displays and i want a little performance so vibecoded this file

import pygame


class Display:
    def __init__(self, width=32, height=32, scale=12):
        self.width = width
        self.height = height
        self.scale = scale

        self.vram = bytearray(width * height)

        pygame.init()

        self.window = pygame.display.set_mode(
            (width * scale, height * scale)
        )

        self.surface = pygame.Surface((width, height))

    def set_pixel(self, x: int, y: int, color: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.vram[y * self.width + x] = color & 0xFF

    def get_pixel(self, x: int, y: int) -> int:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.vram[y * self.width + x]
        return 0

    def flip(self):
        for y in range(self.height):
            row = y * self.width
            for x in range(self.width):
                c = self.vram[row + x]
                self.surface.set_at((x, y), (c, c, c))

        scaled = pygame.transform.scale(
            self.surface,
            (self.width * self.scale, self.height * self.scale)
        )

        self.window.blit(scaled, (0, 0))
        pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit