import pygame
import sys

pygame.init()

BACKGROUND_COLOR = (173, 216, 230)
BUTTON_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Drone GUI")

font = pygame.font.SysFont(None, 30)

def draw_text(text, x, y, color=TEXT_COLOR):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

while True:
    screen.fill(BACKGROUND_COLOR)

    # Left Panel (List of Commands and Drone Info)
    pygame.draw.rect(screen, BACKGROUND_COLOR, (20, 20, 200, 560))
    pygame.draw.rect(screen, TEXT_COLOR, (20, 20, 200, 560), 2)
    pygame.draw.rect(screen, TEXT_COLOR, (30, 30, 180, 300), 2)
    draw_text("LIST OF", 70, 50)
    draw_text("COMMANDS", 55, 80)
    draw_text("BATTERY", 70, 350)
    draw_text("TEMP", 90, 380)
    draw_text("SPEED", 90, 410)

    # Live Camera Feed Area
    pygame.draw.rect(screen, BACKGROUND_COLOR, (240, 20, 540, 450))
    pygame.draw.rect(screen, TEXT_COLOR, (240, 20, 540, 450), 2)
    draw_text("LIVE CAMERA FEED", 400, 230)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
