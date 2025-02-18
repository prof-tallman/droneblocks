import pygame
from collections import deque
class ScrollableCommandList:
    
    def __init__(self, commandList, screen, widthRatio=0.3, height = 300, x=0, y=0):
        '''Class responsbible for rendering the commands the drone still needs to execute.
        Utilized inside UserInterface.py
        Parameters:
            commandList: list of commands for drone.
            screen: screen to render block list on
            widthRatio: Percentage of width list should take up on screen
            x: top left x coordinate of list
            y: top left y coordinate of list
        '''
        self.commandQueue = deque(commandList) #Queue to hold commands
        self.screen = screen #Screen to draw on
        self.widthRatio = widthRatio #Percentage of screen that block list takes up
        self.x = x #Top left x position of list
        self.y = y #Top left y position of list
        self.width = int(screen.get_width() * widthRatio) #Width of list
        self.height = height #Height of list
        self.bgColor = (200, 200, 200)  #Light gray background of list
        self.blockColor = (100, 149, 237)  #Block color. Light blue
        self.currentlyExecutingBlockColor = (255, 100, 100)
        self.textColor = (255, 255, 255)
        self.blockHeight = 100
        self.blockSpacing = 10
        self.scrollY = 0 #Var to keep track of scrolling
        self.maxScroll = max(0, len(commandList) * (self.blockHeight + self.blockSpacing) - self.height) #Ensures scrolling stops when last block in list is reached
        self.font = pygame.font.Font(None, 30)
        
    def draw(self):
        '''Renders the command list on the screen at (self.x, self.y) with fading opacity.'''
        #Recalculate maxScroll
        self.maxScroll = max(0, len(self.commandQueue) * (self.blockHeight + self.blockSpacing) - self.height)
    
        #Determine which commands to display based on scroll position
        startIndex = self.scrollY // (self.blockHeight + self.blockSpacing)
        maxVisibleCommands = (self.height + self.blockHeight + self.blockSpacing - 1) // (self.blockHeight + self.blockSpacing)
    
        visibleCommands = list(self.commandQueue)[startIndex:startIndex + maxVisibleCommands]
    
        for i, command in enumerate(visibleCommands):
            blockY = self.y + i * (self.blockHeight + self.blockSpacing)
    
            #Opacity Calculation for each block
            opacity = max(25, 255 - (i * 100))  #Decrease alpha value for each command in list. If below 0, lowest it can get is 25
    
            #Create a temporary surface for opacity
            block_surface = pygame.Surface((self.width, self.blockHeight), pygame.SRCALPHA)
            
            #Choose block color based on position in list
            if startIndex + i == 0:
                blockColor = self.currentlyExecutingBlockColor 
            else: 
                blockColor = self.blockColor
    
            #Apply the calculated opacity
            block_surface.fill((blockColor[0], blockColor[1], blockColor[2], opacity)) #blockColor[0] is r value in rgb.
    
            #Draw the semi-transparent block
            self.screen.blit(block_surface, (self.x, blockY))
    
            #Render command text
            textSurface = self.font.render(command, True, self.textColor)
            textRect = textSurface.get_rect(center=(self.x + self.width // 2, blockY + self.blockHeight // 2))
    
            #Draw text
            self.screen.blit(textSurface, textRect)


    def dequeue_command(self):
        '''Removes the first command from the queue when executed and resets scroll position to top of list.'''
        if self.commandQueue:
            self.commandQueue.popleft()  #Remove first command in queue
            #Recalculate max scroll based on updated list
            self.maxScroll = max(0, len(self.commandQueue) * (self.blockHeight + self.blockSpacing) - self.height)
            #Prevent scrollY from being greater than maxScroll
            self.scrollY = 0

    def handle_scroll(self, direction):
        '''Handles scrolling up and down within the command list. If you would like to scroll up, pass "up" to method.'''
        if direction == "up":
            self.scrollY = max(0, self.scrollY - (self.blockHeight + self.blockSpacing))
        elif direction == "down":
            self.scrollY = min(self.maxScroll, self.scrollY + (self.blockHeight + self.blockSpacing))
            
    def is_mouse_inside(self, mouseX, mouseY):
        '''Checks if the mouse is within the command list box.'''
        if (self.x <= mouseX and mouseX <= self.x + self.width) and (self.y <= mouseY and mouseY <= self.y + self.height):
            return True
        else:
            return False

if __name__ == "__main__":
    #Testing for module. Press space to simulate removing a block from the commandList
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    commands = ["takeOff1", "fly_forward2", "fly_up3", "fly_down4", "fly_forward5", "fly_up6", "fly_down7", "fly_forward8", "fly_up9", "fly_down10", "land11"]

    
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
                    command_list.dequeue_command()  #Press space to deque item from list


    
        command_list.draw()  #Draw the command list
        pygame.display.flip()  #Update screen
    
    pygame.quit()


        
        
    
