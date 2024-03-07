import numpy
import pygame
import pyvirtualcam

# pygame setup
pygame.init()
pygame.display.set_caption("EDC-Simulator")
screen = pygame.display.set_mode((128, 72))
width = screen.get_width()
height = screen.get_height()
player_pos = pygame.Vector2(width / 2, height / 2)
clock = pygame.time.Clock()

frame_per_second = 30
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

    pygame.draw.circle(screen, "red", player_pos, 2)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        # print("UP")
        player_pos.y -= 1
    if keys[pygame.K_DOWN]:
        # print("DOWN")
        player_pos.y += 1
    if keys[pygame.K_LEFT]:
        # print("LEFT")
        player_pos.x += 1
    if keys[pygame.K_RIGHT]:
        # print("RIGHT")
        player_pos.x -= 1

    # print(player_pos.x, player_pos.y)

    for x in range(width):
        for y in range(height):
            pixel_color = screen.get_at((x, y))
            frame[y, x] = pixel_color[:3]
    camera.send(frame)

    # update() the display to put your work on screen
    pygame.display.update()

    # wait a little bit to make the game run at frame_per_second fps
    clock.tick(frame_per_second)

pygame.quit()
