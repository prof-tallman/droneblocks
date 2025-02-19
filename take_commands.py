import time

class DroneFlight():

    # drone being the drone we set up with someone's flight controller
    def __init__(self, drone):

        self.drone = drone

        # set speed and time flying
        self.distance = 50
        self.rotation = 45
        self.set_time = 2 # seconds

        # Instead of using a loop for going a certain time, we can set a predetermined distance and speed,
        # and have the drone go that distance like 50cm * 2 seconds for 50cm/s over 2 seconds
        self.speed = self.distance * self.set_time
        self.rotate = self.rotation

    """
    
    Example names:
    - Forward
    - Backward
    - Left
    - Right
    - Up
    - Down
    - RotateCW
    - RotateCCW
    - Takeoff
    - Land

    - Hover
    
    """

    # Take command from our list and make drone do it
    def drone_command(self, command):

        # Cardinal Directions
        if command.lower() == "fly_forward":
            self.drone.move_forward(self.speed)
        elif command.lower() == "fly_backward":
            self.drone.move_back(self.speed)
        elif command.lower() == "fly_left":
            self.drone.move_left(self.speed)
        elif command.lower() == "fly_right":
            self.drone.move_right(self.speed)

        # Up / Down
        elif command.lower() == "fly_up":
            self.drone.move_up(self.speed)
        elif command.lower() == "fly_down":
            self.drone.move_down(self.speed)

        # Rotate
        elif command.lower() == "rotate_right":
            self.drone.rotate_clowckwise(self.rotate)
        elif command.lower() == "rotate_left":
            self.drone.rotate_counter_clockwise(self.rotate)

        # Takeoff / Land
        elif command.lower() == "takeoff":
            self.drone.takeoff()
        elif command.lower() == "land":
            self.drone.land()

        # Hover
        else:
            time.sleep(3)