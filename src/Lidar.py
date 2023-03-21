import pygame
import math

class Lidar(pygame.sprite.Sprite):
    def __init__(self, pos, startAngle, endAngle, increment, color):
        super().__init__()
        self.x, self.y = pos
        self.rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
        self.color = color

        self.startAngle = startAngle
        self.endAngle = endAngle    
        self.increment = increment

        count = int(math.degrees(self.endAngle - self.startAngle) / self.increment) + 1
        self.readings = [0] * count 
        self.lasers = []
        for i in range(count):
            self.lasers.append(Laserbeam((self.x, self.y)))

    def laserScan(self, walls):
        currentAngle = math.degrees(self.startAngle)
        for idx, laser in enumerate(self.lasers):
            laser.x = self.x
            laser.y = self.y
            self.readings[idx] = laser.cast((self.x, self.y), math.radians(currentAngle), walls)
            currentAngle += self.increment

        return self.readings
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        for laser in self.lasers:
            laser.draw(screen, self.color)

    def update(self, pos, theta):
        self.x, self.y = pos
        self.startAngle = theta - math.pi/2
        self.endAngle = theta + math.pi/2

class Laserbeam(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.x, self.y = pos
        self.startx, self.starty = pos
        self.rect = pygame.Rect(self.x - 3, self.y - 3, 6, 6)
        
    def cast(self, start, dir, walls):
        dx = math.cos(dir) * 10
        dy = math.sin(dir) * 10

        dd = (((dx)**2 + (dy)**2)**0.5)
        self.startx, self.starty = start

        distance = 0
        hit = False

        while not hit and distance < 500:
            self.x += dx
            self.y -= dy
            self.rect = pygame.Rect(self.x - 3, self.y - 3, 6, 6)

            distance += dd

            if pygame.sprite.spritecollideany(self, walls):
                hit = True

        self.rect = pygame.Rect(self.x - 3, self.y - 3, 6, 6)

        return distance

    def draw(self, screen, color=(0, 0, 0)):
        pygame.draw.rect(screen, color, self.rect)
