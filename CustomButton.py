#-*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:23:18 2025

@author: lasse
"""
import pygame

class Button:
    def __init__(self, x, y, width, height, action, image_path, alt_image_path=None):
        '''Button class
            Parameters:
                x: x coordinate for top left of button
                y: y coordinate for top left of button
                width: width of button
                height: height of button
                image_path: Required. Image to be displayed on button
                alt_image_path: Optional. Image to be displayed once button is clicked.
        
        
        '''
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.clicked = False
        self.alt_image = None
        
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.smoothscale(self.image, (width, height))
            except pygame.error:
                print(f"Error loading image: {image_path}.")
                
        if alt_image_path:
            try:
                self.alt_image = pygame.image.load(alt_image_path).convert_alpha()
                self.alt_image = pygame.transform.smoothscale(self.alt_image, (width, height))
            except pygame.error:
                print(f"Error loading alt image: {alt_image_path}.")
                
    def draw(self, screen):
        
        if self.alt_image and self.clicked:
            screen.blit(self.alt_image, self.rect.topleft)  #Draw the alt image
        else:
            screen.blit(self.image, self.rect.topleft)  #Draw the image
    
    def handle_event(self, event):
        """Handles mouse click events and executes the button's action."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = not self.clicked  #Toggle state
                if self.action:
                    self.action()  #Execute assigned function
                    
    def is_hovered(self, mouse_pos):
        """Returns True if the mouse is hovering over the button."""
        return self.rect.collidepoint(mouse_pos)

if __name__ == "__main__":
    
    def recording_action():
        print("Recording Button clicked")
        
    def stop_action():
        print("Stop Button clicked")
        
    def record_action():
        print("Record Button Clicked")
        
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Button Test")

    #Load button images
    recording_button_image = "icons/StartRecordingCommandBlock.png"
    recording_alt_button_image = "icons/RecordingOnCommandBlock.png"
    stop_button_image = "icons/EStopCommandBlock.png"
    record_button_image = "icons/ToggleCameraOffCommandBlock.png"
    record_alt_button_image = "icons/ToggleCameraOnCommandBlock.png"

    #Create a button instance
    recording_button = Button(50, 200, 100, 100, recording_action, recording_button_image, recording_alt_button_image)
    stop_button = Button(200, 200, 100, 100, stop_action, stop_button_image)
    record_button = Button(350, 200, 100, 100, record_action, record_button_image, record_alt_button_image)
    buttons = [recording_button, stop_button, record_button]
    running = True
    while running:
        screen.fill((30, 30, 30))  #Clear screen
        
        mouse_pos = pygame.mouse.get_pos()
        
        #Check if the cursor should change
        hovering_over_button = any(button.is_hovered(mouse_pos) for button in buttons)
        if hovering_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  #Change to hand cursor
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  #Reset to default cursor

        #Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            recording_button.handle_event(event)
            stop_button.handle_event(event)
            record_button.handle_event(event)
            

        #Draw button
        recording_button.draw(screen)
        stop_button.draw(screen)
        record_button.draw(screen)

        pygame.display.flip()  #Update screen

    pygame.quit()

            
