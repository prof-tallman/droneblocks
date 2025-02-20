import pygame
import cv2
import sys

def play_static_video(video_path, screen, screen_width, screen_height, background_image):
    """Plays a staticy MP4 video in the background until it ends."""
    cap = cv2.VideoCapture(video_path)

    clock = pygame.time.Clock()
    video_running = True

    while cap.isOpened() and video_running:
        ret, frame = cap.read()
        if not ret:
            break  #Stop when the video ends

        #Convert frame from BGR (OpenCV) to RGB (Pygame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        frame_surface = pygame.surfarray.make_surface(frame)

        #Scale the video to match screen size
        frame_surface = pygame.transform.scale(frame_surface, (screen_width, screen_height))

        screen.blit(frame_surface, (0, 0))
        screen.blit(background_image, (0, 0)) 
        pygame.display.update()

        #Allows quiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video_running = False  #Stop video early
                pygame.quit()
                sys.exit()

        clock.tick(30)  #Limit frame rate to 30

    cap.release()
