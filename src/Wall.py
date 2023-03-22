import pygame


class Wall(pygame.sprite.Sprite):
    """
    Represents a non-moving dynamically generated wall with collision
    detection.

    Attributes:
        x: x-coordinate
        y: y-coordinate
        surface: surface representation of wall
        image: image that pygame uses to draw
        rect: rectangle that pygame uses for collision detection
    """
    def __init__(self, pos, color, wallGroup):
        super().__init__(wallGroup)
        self.x, self.y = pos

        self.surface = pygame.Surface((20, 20))
        pygame.draw.rect(self.surface, color,
                         pygame.Rect(self.x, self.y, 20, 20))

        self.image = self.surface

        self.rect = pygame.Rect(self.x, self.y, 20, 20)
