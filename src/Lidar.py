import pygame
import math

# How many units to jump per laserbeam iteration
DELTA_SCALE = 5


class Lidar(pygame.sprite.Sprite):
    def __init__(self, pos, startAngle, endAngle, increment, max_range, walls, color):
        super().__init__()
        self.x, self.y = pos
        self.rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
        self.color = color

        self.startAngle = startAngle
        self.endAngle = endAngle
        self.increment = math.radians(increment)
        self.max_range = max_range

        self.walls = walls

        lidarRange = self.endAngle - self.startAngle
        count = int(lidarRange / self.increment) + 1

        self.readings = [0] * count
        self.lasers = pygame.sprite.Group()
        for i in range(count):
            Laserbeam((self.x, self.y), self.lasers)

    # def laserScan(self, walls):
    #     currentAngle = math.degrees(self.startAngle)
    #     for idx, laser in enumerate(self.lasers):
    #         laser.x = self.x
    #         laser.y = self.y
    #         self.readings[idx] = laser.cast((self.x, self.y),
    #                                         math.radians(currentAngle), walls)
    #         currentAngle += self.increment
    #
    #     return self.readings

    def laserScan(self):
        """
        Does a single sweep of laser beams across surroundings from left to
        right of robot with the current lidar settings.

        Returns:
            List containing laser scan distances.
        """
        currentAngle = self.endAngle

        open = []
        for laser in self.lasers:
            deltas = (math.cos(currentAngle) * DELTA_SCALE,
                      math.sin(currentAngle) * DELTA_SCALE,
                      1 * DELTA_SCALE)

            laser.reinit((self.x, self.y), deltas)
            open.append(laser)

            currentAngle += self.increment

        while open:
            for laser in open:
                laser.cast()
                if laser.distance > self.max_range:
                    open.remove(laser)

            collided = pygame.sprite.groupcollide(
                self.lasers, self.walls, False, False).keys()

            collided = [laser for laser in collided if laser in open]

            for laser in collided:
                open.remove(laser)
        
        return self.getDistances()

    def getDistances(self):
        """
        Read distances from lasers

        Returns:
            List filled with distances going from left of robot to right
        """
        ret = []
        for laser in self.lasers:
            ret.append(laser.distance)

        return ret

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        for laser in self.lasers:
            laser.draw(screen, self.color)
#
    def update(self, pos, theta):
        self.x, self.y = pos
        self.rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
        self.startAngle = theta - math.pi/2
        self.endAngle = theta + math.pi/2


class Laserbeam(pygame.sprite.Sprite):
    def __init__(self, pos, lasers):
        super().__init__(lasers)
        self.x, self.y = pos
        self.startx, self.starty = pos
        self.rect = pygame.Rect(self.x - 3, self.y - 3, 6, 6)

        self.distance = 0
    #
    # def cast(self, start, dir, walls):
    #     dx = math.cos(dir) * 10
    #     dy = math.sin(dir) * 10
    #
    #     dd = (((dx)**2 + (dy)**2)**0.5)
    #     self.startx, self.starty = start
    #
    #     distance = 0
    #     hit = False
    #
    #     while not hit and distance < 500:
    #         self.x += dx
    #         self.y -= dy
    #         self.rect = pygame.Rect(self.x - 3, self.y - 3, 6, 6)
    #
    #         distance += dd
    #
    #         if pygame.sprite.spritecollideany(self, walls):
    #             hit = True
    #
    #     self.rect = pygame.Rect(self.x - 3, self.y - 3, 6, 6)
    #
    #     return distance

    def reinit(self, pos, deltas):
        self.distance = 0
        self.x, self.y = pos
        self.deltas = deltas

    def cast(self):
        self.updatePos()
        self.distance += self.deltas[2]
        self.rect = pygame.Rect(self.x - 3, self.y - 3, 6, 6)

    def updatePos(self):
        self.x += self.deltas[0]
        self.y += self.deltas[1]

    def draw(self, screen, color=(0, 0, 0)):
        pygame.draw.rect(screen, color, self.rect)
