import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "red", player_pos, 10)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        # print("UP")
        player_pos.y -= 1
    if keys[pygame.K_DOWN]:
        # print("DOWN")
        player_pos.y += 1
    if keys[pygame.K_LEFT]:
        # print("LEFT")
        player_pos.x -= 1
    if keys[pygame.K_RIGHT]:
        # print("RIGHT")
        player_pos.x += 1

    # print(player_pos.x, player_pos.y)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # wait a little bit to make the game run at 60 fps
    clock.tick(120)

pygame.quit()
