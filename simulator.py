import numpy
import pygame
import pyvirtualcam

# pygame setup
pygame.init()
pygame.display.set_caption("EDC-Simulator")
screen = pygame.display.set_mode((640, 360))
width = screen.get_width()
height = screen.get_height()
player_pos = pygame.Vector2(width / 2, height / 2)
player_radius = 15
clock = pygame.time.Clock()

frame_per_second = 120
camera = pyvirtualcam.Camera(width=width, height=height, fps=frame_per_second)
frame = numpy.zeros((height, width, 3), numpy.uint8)

running = True

while running:

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    pygame.draw.circle(screen, "red", player_pos, player_radius)

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_pos.y - player_radius > 10:
        # print("UP")
        player_pos.y -= 1
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_pos.y + player_radius < height - 10:
        # print("DOWN")
        player_pos.y += 1
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_pos.x + player_radius < width - 10:
        # print("LEFT")
        player_pos.x += 1
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_pos.x - player_radius > 10:
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