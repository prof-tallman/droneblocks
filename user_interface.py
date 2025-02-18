import pygame
import sys
from ScrollableCommandList import ScrollableCommandList

pygame.init()

#Colors
BACKGROUND_COLOR = (173, 216, 230)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (170, 170, 170)
BUTTON_CLICK_COLOR = (100, 100, 100)
TEXT_COLOR = (0, 0, 0)

#Screen Setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Drone GUI")

#Font Setup
font = pygame.font.SysFont(None, 30)

def draw_text(text, x, y, color=TEXT_COLOR, size=30):
    """Renders text on the screen."""
    font = pygame.font.SysFont(None, size)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

#Start / Stop Button Properties
button_rect = pygame.Rect(540, 600, 200, 50)  #(x, y, width, height)
button_font = pygame.font.Font(None, 36)

#Initial Button State
button_text = "Start"
button_clicked = False  #Tracks the button state

commands = ["takeOff1", "fly_forward2", "fly_up3", "fly_down4", "fly_forward5", "fly_up6", "fly_down7", "fly_forward8", "fly_up9", "fly_down10", "land11"]

command_list = ScrollableCommandList(commands, screen, widthRatio = 0.12, x=50, y=50)


################################################################
#Temporary to display text about removing objects from list
font = pygame.font.Font(None, 36)
text_surface = font.render("Press space to remove element from scrollable list for testing", True, TEXT_COLOR)
text_rect = text_surface.get_rect(center=(700, 500))
################################################################

running = True
while running:  
    screen.fill(BACKGROUND_COLOR)
    
    #Get Mouse Position
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    #Change button color on hover or click
    if button_rect.collidepoint(mouse_pos):
        if mouse_pressed[0]:  #Left-click
            pygame.draw.rect(screen, BUTTON_CLICK_COLOR, button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

    #Render updated button text
    rendered_button_text = button_font.render(button_text, True, TEXT_COLOR)
    screen.blit(rendered_button_text, (button_rect.x + 70, button_rect.y + 10))

    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                button_clicked = not button_clicked  #Toggle state
                button_text = "Stop" if button_clicked else "Start"  #Change text
                print(f"Button clicked! Now: {button_text}")
                
        if event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if command_list.is_mouse_inside(mouse_x, mouse_y):  # Only scroll if inside the box
                if event.y > 0:  # Scroll up
                    command_list.handle_scroll("up")
                elif event.y < 0:  # Scroll down
                    command_list.handle_scroll("down")
        ###################################################################
        #For testing purposes will be removed in final implimentation
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                command_list.dequeue_command()  # Simulate command execution
    screen.blit(text_surface, text_rect)  # Draw text
        ###################################################################
        
    
                
    command_list.draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
