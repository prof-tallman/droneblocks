# Importing the library
import pygame
import os
from user_interface import run_user_interface
 
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def blit(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        font = pygame.font.SysFont('Arial', 20).render(self.text, True, (0, 0, 0))
        screen.blit(font, font.get_rect(center=self.rect.center))

    def check_click(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class Interface:
    def __init__(self):
        """
        Initializes the programming interface for the drone blocks application.
        This method sets up the Pygame environment, initializes the display window,
        and creates a list of Block objects representing different drone commands.
        Attributes:
          running (bool): A flag to indicate if the application is running.
          SIZE (tuple): The size of the display window (width, height).
          screen (pygame.Surface): The display surface for the application.
          background_color (tuple): The RGB color value for the background.
          blocks (list): A list of Block objects representing drone commands.
        """
        pygame.init()
        self.running = True

        self.SIZE = (1280, 700)
        self.screen = pygame.display.set_mode(self.SIZE)
        self.background_color = (0, 0, 50)

        # relative path to icon folder
        self.icons_path = os.path.join(os.path.dirname(__file__), 'icons') 

        # dictionary of icons for each block paired with their action name and relative path to icon folder
        self.icons = {
            "rotate_left": pygame.image.load(os.path.join(self.icons_path, "rotate_left.png")),
            "rotate_right": pygame.image.load(os.path.join(self.icons_path, "rotate_right.png")),
            "fly_forward": pygame.image.load(os.path.join(self.icons_path, "fly_forward.png")),
            "fly_backward": pygame.image.load(os.path.join(self.icons_path, "fly_backward.png")),
            "fly_left": pygame.image.load(os.path.join(self.icons_path, "fly_left.png")),
            "fly_right": pygame.image.load(os.path.join(self.icons_path, "fly_right.png")),
            "fly_up": pygame.image.load(os.path.join(self.icons_path, "fly_up.png")),
            "fly_down": pygame.image.load(os.path.join(self.icons_path, "fly_down.png")),
            "hover": pygame.image.load(os.path.join(self.icons_path, "hover.png")),
            "takeoff": pygame.image.load(os.path.join(self.icons_path, "takeoff.png")),
            "land": pygame.image.load(os.path.join(self.icons_path, "land.png")),
        }


        # scrollable command surface to place blocks
        self.COMMAND_SIZE = (self.SIZE[0] // 2, self.SIZE[1] + 3000) # creating a big scrollable surface
        self.command_scroll_y = self.SIZE[1]
        self.command_surface = pygame.Surface((self.COMMAND_SIZE[0], self.COMMAND_SIZE[1]))

        # TEMPORARY GRADIENT - FOR DEMONSTRATION
        for y in range(self.COMMAND_SIZE[1]):
            color = (
          255 * (self.COMMAND_SIZE[1] - y) // self.COMMAND_SIZE[1],  # Red component
          0,  # Green component
          255 * y // self.COMMAND_SIZE[1]  # Blue component
            )
            pygame.draw.line(self.command_surface, color, (0, y), (self.COMMAND_SIZE[0], y))

        # Run Button initialization
        self.run_button = Button(self.SIZE[0] // 2 + 150, self.SIZE[1] - 120, 150, 50, "Execute", (100, 200, 100), (150, 255, 150))

 
        self.blocks = [
            Block(25, 200, 'rotate_left', icon=self.icons["rotate_left"]),
            Block(150, 200, 'fly_forward', icon=self.icons["fly_forward"]),
            Block(275, 200, 'rotate_right', icon=self.icons["rotate_right"]),
            Block(25, 325, 'fly_left', icon=self.icons["fly_left"]),
            Block(150, 325, 'fly_backward', icon=self.icons["fly_backward"]),
            Block(275, 325, 'fly_right', icon=self.icons["fly_right"]),
            Block(25, 450, 'fly_up', icon=self.icons["fly_up"]),
            Block(150, 450, 'hover', icon=self.icons["hover"]),
            Block(275, 450, 'fly_down', icon=self.icons["fly_down"]),
            Block(87.5, 575, 'takeoff', icon=self.icons["takeoff"]),
            Block(212.5, 575, 'land', icon=self.icons["land"])
        ]

        # Blocks that are currently on the programming side
        self.used_blocks = []
        self.current_block = None
        self.has_land = False
        self.has_takeoff = False

        self.std_block_size = (100, 100)

        # The y axis coordiante of the block when it's at the bottom
        self.block_bottom = self.SIZE[1]-self.std_block_size[1]
        # Using list so that the values can be changed easily
        self.next_position = [self.COMMAND_SIZE[0], self.block_bottom]

    def run(self):
        """
        Main loop for running the program interface.
        It handles the dragging of blocks within the interface and 
        updates their positions accordingly. The loop continues running until 
        the `self.running` attribute is set to False.
        
        Events:
        - MOUSEBUTTONDOWN: Starts dragging a block if the mouse is clicked on it.
        - MOUSEBUTTONUP: Stops dragging a block if the mouse is released on it.
        - MOUSEMOTION: Updates the position of a block if it is being dragged.
        - QUIT: Exits the loop and quits pygame.
        
        The method also calls the `self.draw()` method to update the display 
        and quits pygame when the loop ends.
        """

        while self.running:
            
            # EVENT HANDLING
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False #to actually exit the loop

                # dragging blocks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for block in self.blocks:
                        if block.surface_rectangle.collidepoint(event.pos):

                            # error handling to require takeoff/land and prevent multiple takeoff/land 
                            if block.action == "takeoff" and self.has_takeoff:
                                print("Already have takeoff")
                                continue
                            if block.action == "land" and self.has_land:
                                print("Already have land")
                                continue
                            if block.action != "takeoff" and not self.has_takeoff:
                                print("Need to takeoff first")
                                continue

                            # NOTE: Creates a copy and adds it to the in use blocks
                            copy = block.copy()
                            self.current_block = copy

                    for block in self.used_blocks:
                        # print((block.x, block.y), event.pos)
                        if block.surface_rectangle.collidepoint(event.pos):
                            block.dragging = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    print("MOUSE BUTTON UP")
                    if self.current_block:
                        # Makes sure that the block gets placed on the program side (right)

                        if event.pos[0] >= self.COMMAND_SIZE[0]+self.current_block.width//2:

                            # Moving this operation to draw
                            """print("Moving to ", self.next_position)
                            self.next_position[1] -= self.std_block_size[1]

                            if self.next_position[1] == -self.std_block_size[1]:
                                self.next_position[0] += self.std_block_size[0]
                                self.next_position[1] = self.block_bottom"""

                            self.current_block.x = self.COMMAND_SIZE[0]
                            self.current_block.y = self.block_bottom
                            
                            self.used_blocks.append(self.current_block.copy(drag=False, id=len(self.used_blocks)))

                            # validate and update takeoff/land status
                            actions = [block.action for block in self.used_blocks]
                            self.has_land = True if "land" in actions else False
                            self.has_takeoff = True if "takeoff" in actions else False

                            self.current_block.dragging = False
                            self.current_block = None

                        else:
                            self.current_block.dragging = False 
                            self.current_block = None


                    # Events for already placed blocks
                    for block in self.used_blocks:
                        if block.surface_rectangle.collidepoint(event.pos):
                            if event.pos[0] < self.COMMAND_SIZE[0]+block.width//2:
                                id = block.id
                                for subset_block in self.used_blocks[block.id:]:
                                    subset_block.id -=1

                                del self.used_blocks[id]
                                
                            block.dragging = False

                    print(f"Number of placed blocks: {len(self.used_blocks)}")



                elif event.type == pygame.MOUSEMOTION:
                    for block in self.used_blocks:
                        if block.dragging:
                            mouse_x, mouse_y = event.pos
                            block.x = mouse_x - block.width // 2
                            block.y = mouse_y - block.height // 2
                            block.surface_rectangle.topleft = (block.x, block.y)
                            # print(block.x, block.y)

                    if self.current_block:
                        mouse_x, mouse_y = event.pos
                        self.current_block.x = mouse_x - self.std_block_size[0] // 2
                        self.current_block.y = mouse_y - self.std_block_size[1] // 2

                # scrolling command surface
                elif event.type == pygame.MOUSEWHEEL:
                    if self.used_blocks:
                        self.used_blocks[0].y += event.y*20   

                    if event.y > 0: # scroll up
                        self.command_scroll_y = max(self.command_scroll_y - 30, 0 + self.SIZE[1])
                    elif event.y < 0: # scroll down
                      self.command_scroll_y = min(self.command_scroll_y + 30, self.COMMAND_SIZE[1])


                if self.run_button.check_click(event):
                    commands = [block.action for block in sorted(self.used_blocks, key=lambda b: b.y, reverse=True)]
                    if commands[-1] == 'land':
                        print("Calling run_user_interface")
                        run_user_interface(commands) #Runs user_interface module
                    else:
                        print("Still needs a land block!")

            # BLITTING
            self.draw()

        pygame.quit()

    def draw(self):
        """
        Draws the current state of the screen, uses blit method of the block class to draw each block. As well as the command surface and run button.
        This method fills the screen with the background color, draws a divider between commands and control area.
        """
        self.screen.fill(self.background_color)

        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.SIZE[0]//2 - 2, 0, 1, self.SIZE[1])) # divider between blocks and control area
        
        self.screen.blit(self.command_surface, (self.SIZE[0]//2, self.command_scroll_y - self.COMMAND_SIZE[1]))

        self.run_button.blit(self.screen) 
        

        # Used originally for grid formatted blocks
        """for block in self.used_blocks:
            if not block.dragging and not block.scrolling:

                # Block placement based on ID
                block.y = self.SIZE[1] - ((block.id+1)%7)*block.height - block.height

                block.x = self.COMMAND_SIZE[0] + ( (block.id+1)//7 ) * block.width"""
        
        # Used for scrollable blocks
        # All block placements are based on the previous block
        # The 0th index block retains it's own position which is changed by scrolling
        for i in range(len(self.used_blocks)):
            block = self.used_blocks[i]
                        
            if not block.dragging:
                if block.id == 0:
                    if len(self.used_blocks) == 1:
                        block.y = self.block_bottom - (i * (block.height + 10))
                        block.x = self.COMMAND_SIZE[0] + 20
                        continue
                    else:
                        block.x = self.COMMAND_SIZE[0] + 20
                        continue

                else:
                    block.y = self.used_blocks[i-1].y - block.height - 10
                    block.x = self.COMMAND_SIZE[0] + 20

        starts_with_takeoff = len(self.used_blocks)>0
        if starts_with_takeoff:
            starts_with_takeoff = self.used_blocks[0].action == 'takeoff'

        for block in self.blocks:
            block.active= starts_with_takeoff or block.action == 'takeoff'


        for rect in self.blocks+self.used_blocks:
            
            rect.blit(self.screen)


        if self.current_block:
            self.current_block.blit(self.screen)


        # pygame.display.update() # updates portion of screen if given arguments, else updates whole screen
        pygame.display.flip() # updates whole screen

class Block:
    def __init__(self, x: int, y: int, action: str, id=None, icon = None):
        """
        Initializes a new Block object for the drone programming interface.
        
        Parameters:
            x (int): The x-coordinate of the block's initial position.
            y (int): The y-coordinate of the block's initial position.
            action (str): The action or command represented by the block.
        
        Attributes:
            x (int): The current x-coordinate of the block.
            y (int): The current y-coordinate of the block.
            width (int): The width of the block.
            height (int): The height of the block.
            action (str): The action or command represented by the block.
            dragging (bool): A flag indicating whether the block is being dragged.
            surface (pygame.Surface): The surface representing the block.
            surface_rectangle (pygame.Rect): The rectangle defining the block's position and size.
        """
        self.x = x
        self.y = y
        self.width, self.height = 100, 100
        self.action = action
        self.active = True
        self.dragging = False
        self.id = id
        self.scrolling = False
        self.icon = icon

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Enables transparency
        self.surface.fill((200, 200, 200))

        self.surface_rectangle = self.surface.get_rect() # drawing rectangle exactly to the surface to enable interactivity like collidepoint
        self.surface_rectangle.topleft = (self.x, self.y) 

    def blit(self, screen: pygame.Surface):
        """
        Blits the block's surface onto the screen at its (x, y) coordinates.
        Displays the block's action name when hovered.
        
        Parameters:
          screen (pygame.Surface): The surface to draw the block on.
        """
        self.surface_rectangle.topleft = (self.x, self.y) 
        screen.blit(self.surface, (self.x, self.y))

        # Draws the icons dynamically
        if self.icon and self.active:
            scaled_icon = pygame.transform.scale(self.icon, (self.width, self.height))  # Scale icon
            icon_rect = scaled_icon.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))  # Center icon
            screen.blit(scaled_icon, icon_rect.topleft)  # Blit icon at new position

        self.check_hover(pygame.mouse.get_pos())

        self.surface.fill((100,100,200))
            

        # temporary font so that we can see the names of the blocks
        temp_font = pygame.font.SysFont('Arial', 14).render(self.action, True, (0, 0, 0))
        self.surface.blit(temp_font, (5, 5))
        
    #The rect.collidepoint() method is used to check if a point is inside a rectangle, can use it for highlighting detection
    def check_hover(self, mouse_pos):
        """ 
        Checks if the mouse is hovering over the block and changes its color accordingly. 
        
        Parameters:
          mouse_pos (tuple): The current position of the mouse (x, y).
        """
        if self.surface_rectangle.collidepoint(mouse_pos):
            self.surface.fill((200, 200, 200))
        else:
            self.surface.fill((255, 255, 255))

    def check_click(self, mouse_pos):
        """
        Checks if the block is clicked and prints the action associated with the block.
        
        Parameters:
          mouse_pos (tuple): The current position of the mouse (x, y).
        """
        if self.surface_rectangle.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            print(f"{self.action} clicked")
            

    def copy(self, drag=True, id=None):
        block = Block(self.x, self.y, self.action, id, self.icon)
        block.dragging = drag
        return block
    
    def set_position(self, pos):
        self.x, self.y = pos

if __name__ == "__main__":
    interface = Interface()

    interface.run()
