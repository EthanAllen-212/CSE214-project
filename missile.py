import math 
import stddraw # type: ignore

class Missile:

    SPEED = 0.02

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        angle_rad = math.radians(angle)
        self.vx = self.SPEED * math.cos(angle_rad)
        self.vy = self.SPEED * math.sin(angle_rad)

    def move(self):
        self.x += self.vx
        self.y += self.vy
    
    def off_screen(self):
        return self.x < 0 or self.x > 1 or self.y < 0 or self.y > 1
    
    def draw(self):
        stddraw.filledCircle(self.x, self.y, 0.01)  # Draw the missile as a small circle