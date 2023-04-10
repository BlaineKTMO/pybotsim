import pygame
import os
import math
import torch

from PyBotSim.src.Lidar import Lidar
from PyBotSim.src.World import World
from PyBotSim.src.Robot import Robot
from PyBotSim.src.Wall import Wall
from PyBotSim.src.val.Colors import *

DIMENSIONS = [1600, 1000]
ROBOT_START = [800, 900]
FRAMERATE = 200

map = """
................................................................................
................................................................................
................................................................................
#######################################....#####################################
#######################################....#####################################
#######################################....#####################################
#######################################....#####################################
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
...............##################....#............#.............................
..............#..................##..#............#.............................
.............#.................###########........#.............................
............#.............................#.......#.............................
.........###...............................#......#.............................
........##..........#######.................#.....#.............................
......###............##....###...............#....#.............................
.....##............##.........#...............#...#.............................
....##............#............#...............#..#.............................
................##..............#...............#.#.............................
...............##................#...............##.............................
...............#..................#...............#.............................
..................................####............#.............................
.....................................#............#.............................
.....................................#............#.............................
#....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
.....................................#............#.............................
#....................................#............#.............................
"""

class Simulator:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(FRAMERATE)

        current_path = os.path.dirname(__file__)
        image_path = os.path.join(current_path, 'images')
        robot_img = os.path.join(image_path, 'robot.png')

        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.robotInfoVl = self.font.render('default', True, BLACK, WHITE)
        self.robotInfoVr = self.font.render('default', True, BLACK, WHITE)
        self.robotInfoTheta = self.font.render('default', True, BLACK, WHITE)

        # Get text element rectangles
        self.robotInfoRectVl = self.robotInfoVl.get_rect()
        self.robotInfoRectVr = self.robotInfoVr.get_rect()
        self.robotInfoRectTheta = self.robotInfoTheta.get_rect()

        # Move robot info rectangles to correct position
        self.robotInfoRectVl.center = (DIMENSIONS[0] - 400, DIMENSIONS[1] - 200)
        self.robotInfoRectVr.center = (DIMENSIONS[0] - 400, DIMENSIONS[1] - 150)
        self.robotInfoRectTheta.center = (DIMENSIONS[0] - 400, DIMENSIONS[1] - 100)

        self.world = World(DIMENSIONS)
        self.world.screen.fill(WHITE)
        self.walls = createMap(map)
        self.walls.draw(self.world.screen)

        self.robot = Robot(ROBOT_START, robot_img, 0.01)
        self.lidar = Lidar((self.robot.x, self.robot.y), 0, math.pi, 1, 300, self.walls, GREEN)

    def set_dt(self):
        self.dt = self.clock.tick(FRAMERATE)/1000

    def reset(self):
        self.robot.x, self.robot.y = ROBOT_START

    def update(self):
        # Update calls #
        self.robot.update(self.dt)
        self.lidar.update((self.robot.x, self.robot.y), self.robot.theta)
        self.updateRobotInfo()

        # Draw new screen and add robot info
        self.world.screen.fill(WHITE)
        self.world.screen.blit(self.robotInfoVl, self.robotInfoRectVl)
        self.world.screen.blit(self.robotInfoVr, self.robotInfoRectVr)
        self.world.screen.blit(self.robotInfoTheta, self.robotInfoRectTheta)

        # Draw robot, walls, trail, and LiDAR #
        self.world.draw_trail(self.robot.getPos(), YELLOW)
        self.walls.draw(self.world.screen)
        self.robot.draw(self.world.screen)
        self.lidar.draw(self.world.screen)

        pygame.display.update()

    def updateRobotInfo(self):
        info_vl = f"Vl = {self.robot.vl:.3f}m/s"
        info_vr = f"Vr = {self.robot.vr/self.robot.m2p:.3f}m/s"
        info_theta = f"theta = {math.degrees(self.robot.theta):.3f} degrees"

        self.robotInfoVl = self.font.render(info_vl, True, BLACK, WHITE)
        self.robotInfoVr = self.font.render(info_vr, True, BLACK, WHITE)
        self.robotInfoTheta = self.font.render(info_theta, True, BLACK, WHITE)

    def controllableSim(self):
        _, running = self.forward()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.robot.move(pygame.key.get_pressed())

            self.set_dt()
            self.update()

    def step(self, action=None):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if action:
            self.robot.applyAcceleration(action)

        self.set_dt()
        self.update()

        return (self.lidar.laserscan, running)


def createMap(map):
    x_loc = 0
    y_loc = 0
    walls = pygame.sprite.Group()
    grid = []

    for char in map:
        if char == "\n":
            continue
        grid.append(char)

    for idx, char in enumerate(grid):
        if idx != 0 and idx % 80 == 0:
            x_loc = 0
            y_loc += 20
        else:
            x_loc += 20
        if char == '#':
            Wall((x_loc, y_loc), GREEN, walls)

    return walls


def main():
    pygame.init()

    sim = Simulator()
    sim.controllableSim()

    # clock = pygame.time.Clock()
    # dt = clock.tick(30)
    # # lastTime = pygame.time.get_ticks()
    #
    # current_path = os.path.dirname(__file__)
    # image_path = os.path.join(current_path, 'images')
    # robot_img = os.path.join(image_path, 'robot.png')
    #
    # font = pygame.font.Font('freesansbold.ttf', 30)
    # robotInfoVl = font.render('default', True, BLACK, WHITE)
    # robotInfoVr = font.render('default', True, BLACK, WHITE)
    # robotInfoTheta = font.render('default', True, BLACK, WHITE)
    #
    # # Set text element rectangles
    # robotInfoRectVl = robotInfoVl.get_rect()
    # robotInfoRectVr = robotInfoVr.get_rect()
    # robotInfoRectTheta = robotInfoTheta.get_rect()
    #
    # # Move robot info rectangles to correct position
    # robotInfoRectVl.center = (DIMENSIONS[0] - 400, DIMENSIONS[1] - 200)
    # robotInfoRectVr.center = (DIMENSIONS[0] - 400, DIMENSIONS[1] - 150)
    # robotInfoRectTheta.center = (DIMENSIONS[0] - 400, DIMENSIONS[1] - 100)
    #
    # world = World(DIMENSIONS)
    # world.screen.fill(WHITE)
    # walls = createMap(map)
    # walls.draw(world.screen)
    #
    # robot = Robot(ROBOT_START, robot_img, 0.01)
    # lidar = Lidar((robot.x, robot.y), 0, math.pi, 10, 300, walls, GREEN)
    #
    # # lidar_rate = 20
    # # rate_counter = 0
    #
    # # MAIN SIM LOOP #
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #     robot.move(pygame.key.get_pressed())
    #
    #     # Old time keeping system #
    #     # dt = (pygame.time.get_ticks() - lastTime)/1000
    #     # lastTime = pygame.time.get_ticks()
    #
    #     dt = clock.tick(FRAMERATE)/1000
    #
    #     info_vl = f"Vl = {robot.vl/robot.m2p:.3f}m/s"
    #     info_vr = f"Vr = {robot.vr/robot.m2p:.3f}m/s"
    #     info_theta = f"theta = {math.degrees(robot.theta):.3f} degrees"
    #
    #     robotInfoVl = font.render(info_vl, True, BLACK, WHITE)
    #     robotInfoVr = font.render(info_vr, True, BLACK, WHITE)
    #     robotInfoTheta = font.render(info_theta, True, BLACK, WHITE)
    #
    #     # Deprecated lidar rate #
    #     # if rate_counter == 19:
    #     #     lidar.update((robot.x, robot.y), robot.theta)
    #     #     s = lidar.laserScan()
    #     #     print(s)
    #
    #     # Update calls #
    #     robot.update(dt)
    #     lidar.update((robot.x, robot.y), robot.theta)
    #
    #     # Draw new screen and add robot info
    #     world.screen.fill(WHITE)
    #     world.screen.blit(robotInfoVl, robotInfoRectVl)
    #     world.screen.blit(robotInfoVr, robotInfoRectVr)
    #     world.screen.blit(robotInfoTheta, robotInfoRectTheta)
    #
    #     # Draw robot, walls, trail, and LiDAR #
    #     world.draw_trail(robot.getPos(), YELLOW)
    #     walls.draw(world.screen)
    #     robot.draw(world.screen)
    #     lidar.draw(world.screen)
    #
    #     pygame.display.update()
    #
    #     # Deprecated Lidar rate
    #     # rate_counter += 1
    #     # if rate_counter > lidar_rate:
    #     #     rate_counter = 0
