import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, color, wallGroup):
        super().__init__(wallGroup)
        self.x, self.y = pos

        self.surface = pygame.Surface((20, 20))
        pygame.draw.rect(self.surface, color, pygame.Rect(self.x, self.y, 20, 20))
        
        self.image = self.surface
        
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
