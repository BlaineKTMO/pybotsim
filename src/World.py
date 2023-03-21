import pygame


class World:
    def __init__(self, dimensions):
        self.height = dimensions[1]
        self.width = dimensions[0]
        self.trail_set = []

        pygame.display.set_caption("Differential Drive")

        print("World initialization complete.")

        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_trail(self, pos, color):
        for i in range(0, len(self.trail_set) - 1):
            pygame.draw.line(self.screen, color,
                             (self.trail_set[i][0], self.trail_set[i][1]),
                             (self.trail_set[i+1][0], self.trail_set[i+1][1]),
                             width=5)

        if self.trail_set.__sizeof__() > 60000:
            self.trail_set.pop(0)

        self.trail_set.append(pos)
