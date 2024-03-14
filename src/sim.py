import numpy
import pygame
import pyvirtualcam
import threading

import msg

lock = threading.Lock()

def Sim():

    pygame.init()
    pygame.display.set_caption("EDC-Simulator")

    width = 640
    height = 360
    screen = pygame.display.set_mode((width, height))

    player_pos = pygame.Vector2(width / 2, height / 2)
    player_radius = 15

    clock = pygame.time.Clock()

    frame_per_second = 120
    camera = pyvirtualcam.Camera(width=width, height=height, fps=frame_per_second)
    frame = numpy.zeros((height, width, 3), numpy.uint8)

    running = True

    # cnt = 0

    while running:

        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        pygame.draw.circle(screen, "red", player_pos, player_radius)

        # keys = pygame.key.get_pressed()
        # if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_pos.y - player_radius > 10:
        #     # print("UP")
        #     player_pos.y -= 1
        # if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_pos.y + player_radius < height - 10:
        #     # print("DOWN")
        #     player_pos.y += 1
        # if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_pos.x + player_radius < width - 10:
        #     # print("LEFT")
        #     player_pos.x += 1
        # if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_pos.x - player_radius > 10:
        #     # print("RIGHT")
        #     player_pos.x -= 1

        # cnt += 1
        # cnt = cnt % 1000000
        # if int((cnt % 400) / 100) == 0:
        #     player_pos.y -= 1
        # if int((cnt % 400) / 100) == 1:
        #     player_pos.x += 1
        # if int((cnt % 400) / 100) == 2:
        #     player_pos.y += 1
        # if int((cnt % 400) / 100) == 3:
        #     player_pos.x -= 1

        lock.acquire()
        now_str = msg.now_pos_str
        goal_str = msg.goal_pos_str
        lock.release()

        goal = msg.str_to_pos(goal_str)
        now = msg.str_to_pos(now_str)
        print(goal, now)

        if (goal[0] < now[0]) and player_pos.y - player_radius > 10:
            # print("UP")
            player_pos.y -= 1
        if (goal[0] > now[0]) and player_pos.y + player_radius < height - 10:
            # print("DOWN")
            player_pos.y += 1
        if (goal[1] < now[1]) and player_pos.x + player_radius < width - 10:
            # print("LEFT")
            player_pos.x += 1
        if (goal[1] > now[1]) and player_pos.x - player_radius > 10:
            # print("RIGHT")
            player_pos.x -= 1
        # print(player_pos.x, player_pos.y)

        change_area = [[int(player_pos.x - player_radius - 5), int(player_pos.y - player_radius - 5)],
                       [int(player_pos.x + player_radius + 5), int(player_pos.y + player_radius + 5)]]
        
        for x in range(change_area[0][0], change_area[1][0] + 1):
            for y in range(change_area[0][1], change_area[1][1] + 1):
                pixel_color = screen.get_at((x, y))
                frame[y, x] = pixel_color[:3]
        camera.send(frame)

        # update() the display to put your work on screen
        pygame.display.update()

        # wait a little bit to make the game run at frame_per_second fps
        clock.tick(frame_per_second)

    pygame.quit()