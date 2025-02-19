import pygame
import sys
from ScrollableCommandList import ScrollableCommandList
import threading
import queue
from djitellopy import Tello
import cv2
from take_commands import DroneFlight

pygame.init()

# Drone setup
tello = Tello()
tello.connect()

# Initiate class for giving drone commands
flight = DroneFlight(tello)

# Camera setup
tello.stream_on()

frame_queue = queue.Queue(maxsize=1)  # Limit queue size to avoid lag

def camera_thread():
    """ Thread function to continuously update the camera frame """
    while True:
        frame = tello.get_frame_read().frame
        if frame is not None:
            # Rotate frame to match display
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # Put the frame in the queue (overwrite old frame if queue is full)
            if frame_queue.full():
                frame_queue.get()
            frame_queue.put(frame)

# Start the camera thread
camera_thread = threading.Thread(target=camera_thread, daemon=True)
camera_thread.start()

# How to run camera in game loop
"""
if not frame_queue.empty():
            frame = frame_queue.get()
            # Convert the frame to a Pygame surface
            webcam_surface = pygame.surfarray.make_surface(frame)
            webcam_rect = webcam_surface.get_rect()
            webcam_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(webcam_surface, webcam_rect)
"""

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

background_image = pygame.image.load("icons/background.png")  
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  #Scale it to fit

icon_height = 32
icon_width = 140

#Load status icons
battery_image = pygame.image.load("icons/BatteryBar.png").convert_alpha()
temperature_image = pygame.image.load("icons/TemperatureBar.png").convert_alpha()
speed_image = pygame.image.load("icons/SpeedBar.png").convert_alpha()

#Resize while maintaining aspect ratio
battery_image = pygame.transform.smoothscale(battery_image, (icon_width, icon_height))
temperature_image = pygame.transform.smoothscale(temperature_image, (icon_width, icon_height))
speed_image = pygame.transform.smoothscale(speed_image, (icon_width, icon_height))

#Font Setup
font = pygame.font.SysFont(None, 30)

def draw_text(text, x, y, color=TEXT_COLOR, size=30):
    """Renders text on the screen."""
    font = pygame.font.SysFont(None, size)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

#Start / Stop Button Properties
button_rect = pygame.Rect(400, 620, 200, 50)  #(x, y, width, height)
button_font = pygame.font.Font(None, 36)

#Initial Button State
button_text = "Start"
button_clicked = False  #Tracks the button state

commands = ["takeoff", "fly_forward", "fly_up", "fly_down", "fly_forward", 
            "fly_up", "fly_down", "fly_forward", "fly_up", "fly_down", "land"]
command_list = ScrollableCommandList(commands, screen, widthRatio=0.12, height=400, x=120, y=190)

running = True
while running:  
    pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)) #Replace this line with drone camera feed and logo
    screen.blit(background_image, (0, 0))  #Render background PNG
    screen.blit(battery_image, (1090, 47)) #Render battery status icon
    screen.blit(temperature_image, (1090, 82)) #Render temp status icon
    screen.blit(speed_image, (1090, 117)) #Render speed status icon
    
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
        ###################################################################
        
    
                
    command_list.draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
