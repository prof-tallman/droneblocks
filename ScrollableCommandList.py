import pygame
from collections import deque

class ScrollableCommandList:
    
    def __init__(self, commandList, screen, widthRatio=0.3, height=300, x=0, y=0):
        """Class responsible for rendering the commands the drone still needs to execute.
        Utilized inside UserInterface.py

        Parameters:
            commandList: list of commands for drone.
            screen: screen to render block list on
            widthRatio: Percentage of width list should take up on screen
            x: top left x coordinate of list
            y: top left y coordinate of list
        """
        self.commandQueue = deque(commandList)  #Queue to hold commands
        self.screen = screen  #Screen to draw on
        self.widthRatio = widthRatio  #Percentage of screen that block list takes up
        self.x = x  #Top left x position of list
        self.y = y  #Top left y position of list
        self.width = int(screen.get_width() * widthRatio)  #Width of list
        self.height = height  #Height of list
        self.bgColor = (200, 200, 200)  #Light gray background of list
        self.blockSize = 130
        self.blockSpacing = 10
        self.scrollY = 0  #Var to keep track of scrolling
        self.maxScroll = max(0, len(commandList) * (self.blockSize + self.blockSpacing) - self.height)  #Ensures scrolling stops when last block in list is reached
        self.font = pygame.font.Font(None, 30)
            
    def draw(self):
        """Renders the command list on the screen at (self.x, self.y) with fading opacity."""
        #Recalculate maxScroll
        self.maxScroll = max(0, len(self.commandQueue) * (self.blockSize + self.blockSpacing) - self.height)
    
        #Determine which commands to display based on scroll position
        startIndex = self.scrollY // (self.blockSize + self.blockSpacing)
        maxVisibleCommands = (self.height + self.blockSize + self.blockSpacing - 1) // (self.blockSize + self.blockSpacing)
    
        visibleCommands = list(self.commandQueue)[startIndex:startIndex + maxVisibleCommands]
        
        if self.commandQueue: #Get first command in queue
            first_command = self.commandQueue[0] 
        else: 
            first_command = None


    
        for i, command in enumerate(visibleCommands):
            blockY = self.y + i * (self.blockSize + self.blockSpacing)
    
            #Opacity Calculation for each block
            opacity = max(20, 255 - (i * 120))  #Decrease alpha value for each command in list. Lowest it can get is 20
            newBlocksize = max(50, self.blockSize - (i * 10))
    
            #Load red icon only for the first command in the entire queue
            if command == first_command and startIndex + i == 0:
                image_path = f"icons/{command}_red.png"
            else:
                image_path = f"icons/{command}.png"
    
            try:
                img = pygame.image.load(image_path).convert_alpha()
                img = pygame.transform.smoothscale(img, (newBlocksize, newBlocksize))
            except pygame.error:
                img = None  #If image is missing, set to None
    
            if img:
                #Apply opacity
                img = img.copy()
                img.fill((255, 255, 255, opacity), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(img, (self.x + (self.blockSize - newBlocksize) // 2, blockY)) #Needed to offset change in x when block size changes


    def dequeue_command(self):
        """Removes the first command from the queue when executed and resets scroll position to top of list. Returns the next command in queue"""
        if self.commandQueue:
            self.commandQueue.popleft()  #Remove first command in queue
            #Recalculate max scroll based on updated list
            self.maxScroll = max(0, len(self.commandQueue) * (self.blockSize + self.blockSpacing) - self.height)
            #Prevent scrollY from being greater than maxScroll
            self.scrollY = 0
            
            return self.commandQueue[0] if self.commandQueue else None  #Return next command or None
        return None  #Return None if the queue is already empty
    
    def get_first_command(self):
        return self.commandQueue[0] if self.commandQueue else None  #Return next command or None

    def handle_scroll(self, direction):
        """Handles scrolling up and down within the command list. If you would like to scroll up, pass 'up' to method."""
        if direction == "up":
            self.scrollY = max(0, self.scrollY - (self.blockSize + self.blockSpacing))
        elif direction == "down":
            self.scrollY = min(self.maxScroll, self.scrollY + (self.blockSize + self.blockSpacing))

    def is_mouse_inside(self, mouseX, mouseY):
        """Checks if the mouse is within the command list box."""
        return self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height

    def get_current_command(self):
        """Returns the currently highlighted command based on scroll position."""
        index = self.scrollY // (self.blockSize + self.blockSpacing)
        if 0 <= index < len(self.commandQueue):
            return list(self.commandQueue)[index]
        return None

#Testing for module. Press space to simulate removing a block from the commandList
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Scrollable Command List with Icons")

    commands = ["takeoff", "fly_forward", "fly_up", "fly_down", "fly_forward", 
                "fly_up", "fly_down", "fly_forward", "fly_up", "fly_down", "land"]

    command_list = ScrollableCommandList(commands, screen, x=50, y=50)

    running = True
    while running:
        screen.fill((30, 30, 30))  #Clear screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                #Get current mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                #Check if mouse is inside the command list box
                if command_list.is_mouse_inside(mouse_x, mouse_y):
                    if event.y > 0:  #Scroll up
                        command_list.handle_scroll("up")
                    elif event.y < 0:  #Scroll down
                        command_list.handle_scroll("down")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    command_list.dequeue_command()  #Press space to dequeue item from list

        command_list.draw()  #Draw the command list
        pygame.display.flip()  #Update screen

    pygame.quit()
