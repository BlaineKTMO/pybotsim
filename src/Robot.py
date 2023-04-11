import pygame
import math

class Robot(pygame.sprite.Sprite):
    """

    Attributes: 
        m2p: meter to pixels conversion
        theta: current angle robot is facing
        w: width of robot in pixels.
        vl: left wheel velocity
        vr: right wheel velocity
        image: robot sprite
        rotated: rotated robot sprite
        rect: rect object pygame uses for collision detection
    """
    def __init__(self, startPos, img, diameter):
        super().__init__()
        self.m2p = 10512
        self.x, self.y = startPos
        self.theta = math.pi/2
        self.w = diameter * self.m2p
        self.maxV = 30

        self.vl = 0.00
        self.vr = 0.00

        # self.maxspeed = 0.02 * self.m2p
        # self.minspeed = 0.02 * self.m2p

        self.image = pygame.image.load(img)
        self.rotated = self.image

        self.rect = self.rotated.get_rect(center=(self.x, self.y))

    def getPos(self):
        return (self.x, self.y)

    def adjustVl(self, changeAmount):
        self.vl += changeAmount * self.m2p

    def adjustVr(self, changeAmount):
        self.vr += changeAmount * self.m2p

    def draw(self, screen):
        screen.blit(self.rotated, self.rect)

    def move(self, keys=None):
        """
        User input move method
        Args:
            keys (): key events passed by pygame
        """
        if keys is None:
            return

        if keys[pygame.K_w]:
            self.adjustVl(0.0001)
        if keys[pygame.K_s]:
            self.adjustVl(-0.0001)
        if keys[pygame.K_e]:
            self.adjustVr(0.0001)
        if keys[pygame.K_d]:
            self.adjustVr(-0.0001)

        if (self.vl > self.maxV):
            self.vl = self.maxV
        if (self.vl < -self.maxV):
            self.vl = -self.maxV
        if (self.vr > self.maxV):
            self.vr = self.maxV
        if (self.vr < -self.maxV):
            self.vr = -self.maxV

    def applyAcceleration(self, accel):
        self.vl += accel[0]
        self.vr += accel[1]
        if (self.vl > self.maxV):
            self.vl = self.maxV
        if (self.vl < -self.maxV):
            self.vl = -self.maxV
        if (self.vr > self.maxV):
            self.vr = self.maxV
        if (self.vr < -self.maxV):
            self.vr = -self.maxV

    def update(self, dt):
        """
        Update function
        Args:
            dt (int): miliseconds since last frame 
        """
        self.x += ((self.vl+self.vr)/2) * math.cos(self.theta) * dt
        self.y -= ((self.vl+self.vr)/2) * math.sin(self.theta) * dt
        self.theta += (self.vr-self.vl)/self.w * dt

        if self.theta > 2 * math.pi:
            self.theta = self.theta - 2 * math.pi
        if self.theta < 0:
            self.theta = self.theta + 2 * math.pi

        # Properly rotate robot image
        self.rotated = pygame.transform.rotozoom(
            self.image, math.degrees(self.theta), 1)

        # Set collision rectangle
        self.rect = self.rotated.get_rect(center=(self.x, self.y))
