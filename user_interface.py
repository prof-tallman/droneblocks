import pygame
import sys
from ScrollableCommandList import ScrollableCommandList
from CustomButton import Button
import threading
import queue
from djitellopy import Tello
import cv2
from take_commands import DroneFlight
import math

pygame.init()

# # Drone setup
tello = Tello()
# tello.connect()

# # Initiate class for giving drone commands
# flight = DroneFlight(tello)

# # Camera setup
# tello.stream_on()

# frame_queue = queue.Queue(maxsize=1)  # Limit queue size to avoid lag

# def camera_thread():
#     """ Thread function to continuously update the camera frame """
#     while True:
#         frame = tello.get_frame_read().frame
#         if frame is not None:
#             # Rotate frame to match display
#             frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
#             # Put the frame in the queue (overwrite old frame if queue is full)
#             if frame_queue.full():
#                 frame_queue.get()
#             frame_queue.put(frame)

# # Start the camera thread
# camera_thread = threading.Thread(target=camera_thread, daemon=True)
# camera_thread.start()

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


def recording_action():
    print("Recording Button clicked")
    
def stop_action():
    print("Stop Button clicked")
    
def camera_action():
    print("Camera Button Clicked")

#Colors
BACKGROUND_COLOR = (173, 216, 230)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (170, 170, 170)
BUTTON_CLICK_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)

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

#Load button images
recording_button_image = "icons/StartRecordingCommandBlock.png"
recording_alt_button_image = "icons/RecordingOnCommandBlock.png"
stop_button_image = "icons/EStopCommandBlock.png"
camera_button_image = "icons/ToggleCameraOffCommandBlock.png"
camera_alt_button_image = "icons/ToggleCameraOnCommandBlock.png"

#Create button instances

stop_button = Button(400, 600, 90, 90, stop_action, stop_button_image)
recording_button = Button(525, 600, 90, 90, recording_action, recording_button_image, recording_alt_button_image)
camera_button = Button(650, 600, 90, 90, camera_action, camera_button_image, camera_alt_button_image)
buttons = [recording_button, stop_button, camera_button] #List of buttons used in mouse hover checking


#Font Setup
font = pygame.font.SysFont(None, 30)

def draw_text(text, x, y, color=TEXT_COLOR, size=30):
    """Renders text on the screen."""
    font = pygame.font.SysFont(None, size)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


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
    recording_button.draw(screen) #Render Recording Button
    stop_button.draw(screen)
    camera_button.draw(screen)
    
    #Get Mouse Position
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    
    #Get Drone stats
    try:
        battery_text = f"Battery: {tello.get_battery()}%"
    except Exception:
        battery_text = "na"
    try:
        temperature_text = f"{tello.get_temperature()} °C"
    except Exception:
        temperature_text = "na"
    try:
        speed_x = tello.get_speed_x()
        speed_y = tello.get_speed_y()
        speed_z = tello.get_speed_z()
        
        speed = math.sqrt(speed_x**2 + speed_y**2 + speed_z**2)  #Calculate magnitude
        speed = round(speed, 2)
        speed_text = f"{speed} m/s"
    except Exception:
        speed_text = "na"
        
    #Draw drone stats
    draw_text(battery_text, 1175, 61, size=17)
    draw_text(temperature_text, 1175, 96, size=17)
    draw_text(speed_text, 1175, 131, size=17)
    #Check if the cursor should change on button hover
    hovering_over_button = any(button.is_hovered(mouse_pos) for button in buttons)
    if hovering_over_button:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  #Change to hand cursor
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  #Reset to default cursor

    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                
        if event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if command_list.is_mouse_inside(mouse_x, mouse_y):  # Only scroll if inside the box
                if event.y > 0:  # Scroll up
                    command_list.handle_scroll("up")
                elif event.y < 0:  # Scroll down
                    command_list.handle_scroll("down")
                    
        recording_button.handle_event(event)
        stop_button.handle_event(event)
        camera_button.handle_event(event)
        
        ###################################################################
        #For testing purposes will be removed in final implimentation
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                command_list.dequeue_command()  # Simulate command execution
            if event.key == pygame.K_ESCAPE:
                running = False
        ###################################################################
        
    
    #Draw Command List
    command_list.draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
