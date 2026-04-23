import math
import stddraw  # type: ignore
from missile import Missile  # type: ignore

class Shooter:

    TURRET_LENGTH = 0.07  
    MOVE_SPEED = 0.01
    COOLDOWN = 10     
    WIDTH = 0.06    
    HEIGHT = 0.07   

    def __init__(self, x, y):
        self.x = x                 
        self.y = y                 
        self.velocity = 0          
        self.turret_angle = 90     
        self.recharge_time = 0     

    def update(self, left=0.0, right=1.0):
        self.x += self.velocity
        if self.x < left: self.x = left
        elif self.x > right: self.x = right
        if self.recharge_time > 0: self.recharge_time -= 1

    def controls(self, button):
        if button == 'a': self.velocity = -self.MOVE_SPEED
        elif button == 'd': self.velocity = self.MOVE_SPEED
        elif button == 's': self.velocity = 0

    def shoot(self):
        if self.recharge_time > 0: return None
        angle_rad = math.radians(self.turret_angle)
        tip_x = self.x + self.TURRET_LENGTH * math.cos(angle_rad)
        tip_y = self.y + self.TURRET_LENGTH * math.sin(angle_rad)
        self.recharge_time = self.COOLDOWN
        return Missile(tip_x, tip_y, self.turret_angle)

    def draw(self):
        # 1. SIDE WINGS (Aggressive Red Triangles)
        stddraw.setPenColor(stddraw.RED)
        # Left Wing
        stddraw.filledPolygon([self.x - 0.02, self.x - 0.07, self.x - 0.02], 
                             [self.y + 0.02, self.y - 0.03, self.y - 0.01])
        # Right Wing
        stddraw.filledPolygon([self.x + 0.02, self.x + 0.07, self.x + 0.02], 
                             [self.y + 0.02, self.y - 0.03, self.y - 0.01])

        # 2. MAIN HULL (Deep Blue Fuselage)
        stddraw.setPenColor(stddraw.BOOK_BLUE)
        hull_x = [self.x - 0.025, self.x, self.x + 0.025, self.x]
        hull_y = [self.y - 0.01, self.y + self.HEIGHT, self.y - 0.01, self.y - 0.02]
        stddraw.filledPolygon(hull_x, hull_y)

        # 3. COCKPIT (Black glass for a "stealth" look)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledCircle(self.x, self.y + 0.025, 0.012)

        # 4. ENGINE GLOW (Red Thrusters)
        stddraw.setPenColor(stddraw.RED)
        stddraw.filledCircle(self.x - 0.015, self.y - 0.015, 0.006)
        stddraw.filledCircle(self.x + 0.015, self.y - 0.015, 0.006)
        
        # 5. NOSE CANNON (Small White Tip)
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.filledCircle(self.x, self.y + self.HEIGHT, 0.005)

