import pygame
import math

# How many units to jump per laserbeam iteration
DELTA_SCALE = 10


class Lidar(pygame.sprite.Sprite):
    """

    Attributes: 
        x: x-coordinate
        y: y-coordinate
        rect: Rectangle object used by pygame for collisions
        color: Color of lidar and lidar point cloud
        startAngle: Starting angle of lidar FOV
        endAngle: Ending angle of lidar FOV
        increment: Angle between lidar readings in degrees
        max_range: Maximum distance range of 
        scanning: If the lidar is currently commiting a scan
        open: Laserbeams that have stukk
        laserscan: Output feed of laserscan data
        walls: Sprite group of walls for collision detection
        lasers: Sprite group of lasers
    """
    def __init__(self, pos, startAngle, endAngle, increment, max_range, walls, color):
        super().__init__()
        self.x, self.y = pos
        self.rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
        self.color = color

        self.startAngle = startAngle
        self.endAngle = endAngle
        self.increment = math.radians(increment)
        self.max_range = max_range
        self.delta_scale = DELTA_SCALE

        lidarRange = self.endAngle - self.startAngle
        count = int(lidarRange / self.increment) + 1

        self.scanning = False
        self.open = pygame.sprite.Group()
        self.laserscan = [0] * count

        self.walls = walls

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

    # def laserScan(self):
    #     """
    #     Does a single sweep of laser beams across surroundings from left to
    #     right of robot with the current lidar settings.
    #
    #     Returns:
    #         List containing laser scan distances.
    #     """
    #     currentAngle = self.endAngle
    #
    #     open = pygame.sprite.Group()
    #     for laser in self.lasers:
    #         deltas = (math.cos(currentAngle) * DELTA_SCALE,
    #                   math.sin(currentAngle) * DELTA_SCALE,
    #                   1 * DELTA_SCALE)
    #
    #         laser.reinit((self.x, self.y), deltas)
    #         open.add(laser)
    #
    #         currentAngle += self.increment
    #
    #     while open:
    #         for laser in open:
    #             laser.cast()
    #             if laser.distance > self.max_range:
    #                 open.remove(laser)
    #
    #         collided = pygame.sprite.groupcollide(
    #             open, self.walls, False, False).keys()
    #
    #         for laser in collided:
    #             open.remove(laser)
    #     
    #     return self.getDistances()

    def startScan(self):
        currentAngle = self.startAngle

        for laser in self.lasers:
            deltas = (math.cos(currentAngle) * self.delta_scale,
                      math.sin(currentAngle) * self.delta_scale,
                      1 * self.delta_scale)

            laser.reinit((self.x, self.y), deltas)
            self.open.add(laser)

            currentAngle += self.increment

        self.scanning = True

    def awaitScan(self):
        for laser in self.open:
            if laser.update() > self.max_range:
                self.open.remove(laser)

        collided = pygame.sprite.groupcollide(
            self.open, self.walls, False, False).keys()

        for laser in collided:
            self.open.remove(laser)

        if not self.open:
            self.scanning = False
            self.laserscan = self.getDistances()

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

    def update(self, pos, theta):
        self.x, self.y = pos
        self.rect.center = (self.x, self.y)
        self.startAngle = -theta - math.pi/2
        self.endAngle = -theta + math.pi/2

        if self.scanning:
            self.awaitScan()
        else:
            self.startScan()


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

    def update(self):
        self.x += self.deltas[0]
        self.y += self.deltas[1]
        self.distance += self.deltas[2]
        self.rect.center = (self.x, self.y)

        return self.distance

    def draw(self, screen, color=(0, 0, 0)):
        pygame.draw.rect(screen, color, self.rect)
