import pygame
import sys

pygame.init()

# Colors
BACKGROUND_COLOR = (173, 216, 230)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (170, 170, 170)
BUTTON_CLICK_COLOR = (100, 100, 100)
TEXT_COLOR = (0, 0, 0)

# Screen Setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Drone GUI")

# Font Setup
font = pygame.font.SysFont(None, 30)

def draw_text(text, x, y, color=TEXT_COLOR, size=30):
    """Renders text on the screen."""
    font = pygame.font.SysFont(None, size)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Start / Stop Button Properties
button_rect = pygame.Rect(540, 600, 200, 50)  # (x, y, width, height)
button_font = pygame.font.Font(None, 36)

# Initial Button State
button_text = "Start"
button_clicked = False  # Tracks the button state

running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # Get Mouse Position
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # Change button color on hover or click
    if button_rect.collidepoint(mouse_pos):
        if mouse_pressed[0]:  # Left-click
            pygame.draw.rect(screen, BUTTON_CLICK_COLOR, button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

    # Render updated button text
    rendered_button_text = button_font.render(button_text, True, TEXT_COLOR)
    screen.blit(rendered_button_text, (button_rect.x + 70, button_rect.y + 10))

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                button_clicked = not button_clicked  # Toggle state
                button_text = "Stop" if button_clicked else "Start"  #Change text
                print(f"Button clicked! Now: {button_text}")

    pygame.display.flip()

pygame.quit()
sys.exit()
