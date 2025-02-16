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

        self.SIZE = (1280, 700)
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

        # Blocks that are currently on the programming side
        self.used_blocks = []
        self.current_block = None

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

                # dragging blocks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for block in self.blocks:
                        if block.surface_rectangle.collidepoint(event.pos):
                            # NOTE: Creates a copy and adds it to the in use blocks
                            copy = block.copy()
                            self.current_block = copy

                            # Commented this out since we won't want to be moving blocks that are on display
                            # block.dragging = True

                    for block in self.used_blocks:
                        # print((block.x, block.y), event.pos)
                        # block.dragging = True
                        if block.surface_rectangle.collidepoint(event.pos):
                            block.dragging = True

                elif event.type == pygame.MOUSEBUTTONUP:

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
                            # if block.surface_rectangle.collidepoint(event.pos):
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
                    #for block in self.used_blocks:
                    #   block.scrolling = True
                    self.used_blocks[0].y += event.y*20   

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
                        block.y = self.block_bottom
                        block.x = self.COMMAND_SIZE[0]
                        continue

                else:
                    block.y = self.used_blocks[i-1].y - block.height    
                    block.x = self.COMMAND_SIZE[0]


        for rect in self.blocks+self.used_blocks:
            rect.blit(self.screen)


        if self.current_block:
            self.current_block.blit(self.screen)


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
    def __init__(self, x: int, y: int, action: str, id=None):
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
        self.id = id
        self.scrolling = False

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
            

    def copy(self, drag=True, id=None):
        block = Block(self.x, self.y, self.action, id)
        block.dragging = drag
        return block
    
    def set_position(self, pos):
        self.x, self.y = pos

if __name__ == "__main__":
    interface = Interface()

    interface.run()
