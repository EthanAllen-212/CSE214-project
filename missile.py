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

    def update(self):
        self.x += self.vx
        self.y += self.vy
    
    def off_screen(self):
        # Checks if the missile has left the canvas bounds
        return self.x < 0 or self.x > 1 or self.y < 0 or self.y > 1
    
    def draw(self):
        # Draw the outer circle (Orange Glow)
        stddraw.setPenColor(stddraw.ORANGE)
        stddraw.filledCircle(self.x, self.y, 0.01)
        
        # Draw the inner circle (Black Core)
        # Radius 0.007 leaves a nice 0.003 orange border
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledCircle(self.x, self.y, 0.007)

