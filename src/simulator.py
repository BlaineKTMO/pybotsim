import pygame
import os
import math
from src.Lidar import Lidar
from src.World import World
from src.Robot import Robot
from src.Wall import Wall
from src.val.Colors import *

DIMENSIONS = [1600, 1000]
ROBOT_DIM = [800, 900]

map = """
................................................................................
................................................................................
................................................................................
#######################################....#####################################
#######################################....#####################################
#######################################....#####################################
#######################################....#####################################
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
#.....................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
......................................#............#............................
#.....................................#............#............................
"""

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
    print("Hello world")
    pygame.init()

    clock = pygame.time.Clock()
    dt = clock.tick(30)
    # lastTime = pygame.time.get_ticks()

    current_path = os.path.dirname(__file__)
    image_path = os.path.join(current_path, 'images')
    robot_img = os.path.join(image_path, 'robot.png')

    font = pygame.font.Font('freesansbold.ttf', 30)
    robotInfoVl = font.render('default', True, BLACK, WHITE)
    robotInfoVr = font.render('default', True, BLACK, WHITE)
    robotInfoTheta = font.render('default', True, BLACK, WHITE)

    # Set text element rectangles
    robotInfoRectVl = robotInfoVl.get_rect()
    robotInfoRectVr = robotInfoVr.get_rect()
    robotInfoRectTheta = robotInfoTheta.get_rect()

    # Move robot info rectangles to correct position  
    robotInfoRectVl.center = (DIMENSIONS[0] - 400, DIMENSIONS[1] - 200)
    robotInfoRectVr.center = (DIMENSIONS[0] - 400, DIMENSIONS[1] - 150)
    robotInfoRectTheta.center = (DIMENSIONS[0] - 400, DIMENSIONS[1] - 100)

    world = World(DIMENSIONS) 
    world.screen.fill(WHITE)
    walls = createMap(map)
    walls.draw(world.screen)

    robot = Robot(ROBOT_DIM, robot_img, 0.01)
    lidar = Lidar((robot.x, robot.y), 0, math.pi, 2, 300, walls, GREEN)

    lidar_rate = 20;
    rate_counter = 0;

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        robot.move(pygame.key.get_pressed())
        
        # dt = (pygame.time.get_ticks() - lastTime)/1000
        # lastTime = pygame.time.get_ticks()
        dt = clock.tick(60)/1000
        
        info_vl = f"Vl = {robot.vl/robot.m2p:.3f}m/s"
        info_vr = f"Vr = {robot.vr/robot.m2p:.3f}m/s"
        info_theta = f"theta = {math.degrees(robot.theta):.3f} degrees"

        robotInfoVl = font.render(info_vl, True, BLACK, WHITE)
        robotInfoVr = font.render(info_vr, True, BLACK, WHITE)
        robotInfoTheta = font.render(info_theta, True, BLACK, WHITE)


        robot.update(dt)
        if rate_counter == 19:
            lidar.update((robot.x, robot.y), robot.theta)
            s = lidar.laserScan()
            print(s)

        # lidar.update((robot.x, robot.y), robot.theta)
        # lidar.laserScan()

        world.screen.fill(WHITE)
        walls.draw(world.screen)
        world.screen.blit(robotInfoVl, robotInfoRectVl)
        world.screen.blit(robotInfoVr, robotInfoRectVr)
        world.screen.blit(robotInfoTheta, robotInfoRectTheta)

        world.draw_trail(robot.getPos(), YELLOW)
        robot.draw(world.screen)
        lidar.draw(world.screen)

        pygame.draw.line(world.screen, YELLOW, (1000, 500), (1200, 500))
        pygame.display.update()

        rate_counter += 1
        if rate_counter > lidar_rate:
            rate_counter = 0

