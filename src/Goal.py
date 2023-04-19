import pygame

class Goal(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.x, self.y = pos
        self.pos = pos

        self.surface = pygame.Surface((10, 10))
        pygame.draw.rect(self.surface, color,
                         pygame.Rect(self.x, self.y, 10, 10))

        self.image = self.surface
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
