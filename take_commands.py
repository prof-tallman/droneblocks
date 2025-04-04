import time

class DroneFlight():

    # drone being the drone we set up with someone's flight controller
    def __init__(self, drone):

        self.drone = drone

        # set speed and time flying
        self.distance = 95
        self.rotate = 45

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
            self.drone.move_forward(self.distance)
        elif command.lower() == "fly_backward":
            self.drone.move_back(self.distance)
        elif command.lower() == "fly_left":
            self.drone.move_left(self.distance)
        elif command.lower() == "fly_right":
            self.drone.move_right(self.distance)

        # Up / Down
        elif command.lower() == "fly_up":
            self.drone.move_up(self.distance)
        elif command.lower() == "fly_down":
            self.drone.move_down(self.distance)

        # Rotate
        elif command.lower() == "rotate_right":
            self.drone.rotate_clockwise(self.rotate)
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

    # testing
    def test_command(self, command):

        # Cardinal Directions
        if command.lower() == "fly_forward":
            print("forward")
        elif command.lower() == "fly_backward":
            print("backward")
        elif command.lower() == "fly_left":
            print("left")
        elif command.lower() == "fly_right":
            print("right")

        # Up / Down
        elif command.lower() == "fly_up":
            print("up")
        elif command.lower() == "fly_down":
            print("down")

        # Rotate
        elif command.lower() == "rotate_right":
            print("cw")
        elif command.lower() == "rotate_left":
            print("ccw")

        # Takeoff / Land
        elif command.lower() == "takeoff":
            print("takeoff")
        elif command.lower() == "land":
            print("land")

        # Hover
        else:
            time.sleep(3)