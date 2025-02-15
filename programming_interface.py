# Importing the library
import pygame
 
 
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

        self.SIZE = (1280, 720)
        self.screen = pygame.display.set_mode(self.SIZE)
        self.background_color = (0, 0, 50)

        # scrollable command surface to place blocks
        self.COMMAND_SIZE = (self.SIZE[0] // 2, self.SIZE[1] + 500) ### REMOVE 500 - TEMPORARY FOR DEMONSTRATION
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

 
        self.blocks = [
            Block(25, 200, 'rotate_ccw'),
            Block(150, 200, 'fly_forward'),
            Block(275, 200, 'rotate_cw'),
            Block(25, 325, 'fly_left'),
            Block(150, 325, 'fly_backward'),
            Block(275, 325, 'fly_right'),
            Block(25, 450, 'fly_up'),
            Block(150, 450, 'hover'),
            Block(275, 450, 'fly_down'),
            Block(87.5, 575, 'takeoff'),
            Block(212.5, 575, 'land')
        ]

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

                # dragging blocks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for block in self.blocks:
                        if block.surface_rectangle.collidepoint(event.pos):
                            block.dragging = True
                            print(block.dragging)
                elif event.type == pygame.MOUSEBUTTONUP:
                    for block in self.blocks:
                        if block.surface_rectangle.collidepoint(event.pos):
                            block.dragging = False
                            print(block.dragging)
                elif event.type == pygame.MOUSEMOTION:
                    for block in self.blocks:
                        if block.dragging:
                            if block.surface_rectangle.collidepoint(event.pos):
                                mouse_x, mouse_y = event.pos
                                block.x = mouse_x - block.width // 2
                                block.y = mouse_y - block.height // 2
                                block.surface_rectangle.topleft = (block.x, block.y)
                                print(block.x, block.y)

                # scrolling command surface
                elif event.type == pygame.MOUSEWHEEL:
                  if event.y > 0: # scroll up
                    self.command_scroll_y = max(self.command_scroll_y - 30, 0 + self.SIZE[1])
                  elif event.y < 0: # scroll down
                    self.command_scroll_y = min(self.command_scroll_y + 30, self.COMMAND_SIZE[1])

                elif event.type == pygame.QUIT:
                    self.running = False #to actually exit the loop

            # BLITTING
            self.draw()

        pygame.quit()

    def draw(self):
        """
        Draws the current state of the screen, uses blit method of the block class to draw each block.
        This method fills the screen with the background color, draws a divider between commands and control area.
        """
        self.screen.fill(self.background_color)

        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.SIZE[0]//2 - 2, 0, 1, self.SIZE[1])) # divider between blocks and control area
        
        self.screen.blit(self.command_surface, (self.SIZE[0]//2, self.command_scroll_y - self.COMMAND_SIZE[1]))
        
        for rect in self.blocks:
            rect.blit(self.screen)

        # pygame.display.update() # updates portion of screen if given arguments, else updates whole screen
        pygame.display.flip() # updates whole screen

    def add_block(self, block):
        """
        Adds a new block to the list of commands

        Parameters:
          block (Block): The block to add to the interface.
        """
        # adjusting the height of the command surface
        padding = 10
        new_height = self.COMMAND_SIZE[1] + block.height + padding
        self.command_surface = pygame.Surface((self.COMMAND_SIZE[0], new_height))
         
    def remove_block(self, block):
        """
        Removes a block from the list of commands

        Parameters:
          block (Block): The block to remove from the interface.
        """
        # adjusting the height of the command surface
        padding = 10
        new_height = self.COMMAND_SIZE[1] - block.height - padding
        self.command_surface = pygame.Surface((self.COMMAND_SIZE[0], new_height))

class Block:
    def __init__(self, x: int, y: int, action: str):
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
        color = (255,255,255)
        
        self.x = x
        self.y = y
        self.width, self.height = 100, 100
        self.action = action
        self.dragging = False

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
        screen.blit(self.surface, (self.x, self.y))
        
        self.check_hover(pygame.mouse.get_pos())
        # self.check_click(pygame.mouse.get_pos())

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
            


if __name__ == "__main__":
    interface = Interface()

    interface.run()
