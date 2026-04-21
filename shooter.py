import math
import stddraw  # type: ignore
from missile import Missile  # type: ignore

class Shooter:

    TURRET_LENGTH = 0.06
    MOVE_SPEED = 0.01
    ROTATE_SPEED = 3  # DEGREES per frame
    COOLDOWN = 10  # frames until the next shot can be fired
    WIDTH = 0.05
    HEIGHT = 0.04

    def __init__(self, x, y):
        self.x = x                 # horizontal position 
        self.y = y                 # vertical position
        self.velocity = 0       # controlled by A/S/D buttons
        self.turret_angle = 90     # pointing straight up
        self.recharge_time = 0     # time until next shot can be fired

    def update(self, left=0.0, right=1.0):
        self.x += self.velocity

        # Keep the shooter within the bounds of the screen
        if self.x < left:
            self.x = left
        elif self.x > right:
            self.x = right

        # Decrease recharge time if it's greater than 0
        if self.recharge_time > 0:
            self.recharge_time -= 1

    def controls(self, button):
        if button == 'a':
            self.velocity = -self.MOVE_SPEED  # Move left
        elif button == 'd':
            self.velocity = self.MOVE_SPEED  # Move right
        elif button == 's':
            self.velocity = 0   # Stop moving

        # for rotating the turret
        elif button == ',':
            self.turret_angle = min(180, self.turret_angle + self.ROTATE_SPEED)  # Rotate turret left
        elif button == '.':
            self.turret_angle = max(0, self.turret_angle - self.ROTATE_SPEED)  # Rotate turret right

    def shoot(self):
        # Return a missile object if the shooter can fire, otherwise return None
        if self.recharge_time > 0:
            return None 
        angle_rad = math.radians(self.turret_angle)
        tip_x = self.x + self.TURRET_LENGTH * math.cos(angle_rad)
        tip_y = self.y + self.TURRET_LENGTH * math.sin(angle_rad)
        self.recharge_time = self.COOLDOWN  # Reset recharge time
        return Missile(tip_x, tip_y, self.turret_angle)  # Create a new missile at the tip of the turret
    
    def draw(self):
        stddraw.filledRectangle(self.x - self.WIDTH, self.y, self.WIDTH * 2, self.HEIGHT)  # Draw the base of the shooter

        stddraw.filledCircle(self.x, self.y + self.HEIGHT, self.WIDTH * 0.3) # Base of the turret (a circle on top of the rectangle)

        # the barrel of the turret 
        angle_rad = math.radians(self.turret_angle)
        tip_x = self.x + self.TURRET_LENGTH * math.cos(angle_rad)
        tip_y = (self.y + self.HEIGHT) + self.TURRET_LENGTH * math.sin(angle_rad)
        stddraw.line(self.x, self.y + self.HEIGHT, tip_x, tip_y)  # Draw the turret as a line from the center to the tip
        
