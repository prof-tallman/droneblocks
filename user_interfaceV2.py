import pygame
import sys
from ScrollableCommandList import ScrollableCommandList
from CustomButton import Button
import threading
import queue
from djitellopy import Tello
import cv2
from take_commands import DroneFlight
from Custom_Video_Player import play_static_video
import time #needed for time.sleep(1) with autoscroll commands

class DroneControlApp:
    def __init__(self, commands):
        self.commands = commands
        self.camera_toggle = True
        self.camera_running = True
        self.frame_queue = queue.Queue(maxsize=1)
        self.tello = Tello()
        self.tello.connect()
        self.flight = DroneFlight(self.tello)
        self.tello.streamon()

        pygame.init()
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("sounds/button_press.wav")
        self.alert_sound = pygame.mixer.Sound("sounds/alert.mp3")
        self.startup_sound = pygame.mixer.Sound("sounds/startup.mp3")
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 700
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Drone GUI")
        self.background_image = pygame.image.load("icons/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.command_list = ScrollableCommandList(self.commands, self.screen, widthRatio=0.12, height=400, x=120, y=190)
        pygame.mixer.Sound.play(self.startup_sound)
        

        self.stop_button = Button(400, 600, 90, 90, self.stop_action, "icons/EStopCommandBlock.png")
        self.recording_button = Button(525, 600, 90, 90, self.recording_action, "icons/StartRecordingCommandBlock.png", "icons/RecordingOnCommandBlock.png")
        self.camera_button = Button(650, 600, 90, 90, self.camera_action, "icons/ToggleCameraOnCommandBlock.png", "icons/ToggleCameraOffCommandBlock.png")
        self.buttons = [self.recording_button, self.stop_button, self.camera_button]

        self.camera_thread = threading.Thread(target=self.camera_thread, daemon=True)

        self.running = True

    def stop_action(self):
        pygame.mixer.Sound.play(self.alert_sound)
        print("Stop Button clicked")

    def recording_action(self):
        pygame.mixer.Sound.play(self.click_sound)
        print("Recording Button clicked")

    def camera_action(self):
        pygame.mixer.Sound.play(self.click_sound)
        self.camera_toggle = not self.camera_toggle
        print(f"Camera Toggle {self.camera_toggle}")

    def camera_thread(self):
        while self.camera_running:
            frame = self.tello.get_frame_read().frame
            if frame is not None:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                frame = cv2.flip(frame, 0)
                if self.frame_queue.full():
                    self.frame_queue.get()
                self.frame_queue.put(frame)

    def run(self):

        self.camera_thread.start()
        play_static_video("media/static.mp4", self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.background_image)

        try:
            while self.running:
                self.handle_display()
                self.handle_events()
                pygame.display.flip()
        except KeyboardInterrupt:
            print("Force Quiting Program due to interupt...")
        finally:
            self.cleanup()

    def handle_display(self):
        if self.camera_toggle and not self.frame_queue.empty():
            frame = self.frame_queue.get()
            webcam_surface = pygame.surfarray.make_surface(frame)
            webcam_rect = webcam_surface.get_rect()
            webcam_rect.center = (840, 365)
            self.screen.blit(webcam_surface, webcam_rect)
        else:
            pygame.draw.rect(self.screen, (173, 216, 230), (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(self.background_image, (0, 0))
        for button in self.buttons:
            button.draw(self.screen)
        self.command_list.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEWHEEL:
                self.handle_scroll(event)
            for button in self.buttons:
                button.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.execute_current_command()  # Execute the currently highlighted command
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def handle_scroll(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.command_list.is_mouse_inside(mouse_x, mouse_y):
            if event.y > 0:
                self.command_list.handle_scroll("up")
            elif event.y < 0:
                self.command_list.handle_scroll("down")
            self.execute_current_command()

    def execute_current_command(self):
        """Get the currently highlighted command and execute it using DroneFlight."""
        current_command = self.command_list.get_current_command()
        if current_command:
            print(f"Executing command: {current_command}")
            self.flight.test_command(current_command)  # Use test_command for testing

    def cleanup(self):
        self.camera_running = False
        self.camera_thread.join()
        try:
            self.tello.streamoff()
            self.tello.end()
        except Exception as e:
            print(f"Error closing Tello connection: {e}")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    commands = ["takeoff", "fly_forward", "fly_up", "fly_down", "fly_forward", 
                "fly_up", "fly_down", "fly_forward", "fly_up", "fly_down", "land"]
    app = DroneControlApp(commands)
    app.run()