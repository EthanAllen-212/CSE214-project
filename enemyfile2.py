import stddraw
import math

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0.025
        self.is_alive = True
        # Track direction: 1 for right, -1 for left
        self.direction = 1 

    def move(self, dx, dy):
        #Moves the enemy based on the grid's current velocity
        if not self.is_alive:
            return
        self.x += dx
        self.y += dy

    def draw(self):
        #Draws the enemy only if it hasn't been destroyed.
        if not self.is_alive:
            return

        # Requirement: Drawing enemies 
        stddraw.setPenColor(stddraw.RED)
        stddraw.filledCircle(self.x, self.y, self.radius)

        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledCircle(self.x, self.y, 0.01)

    def check_collision(self, missile_x, missile_y, missile_radius):
        """Checks if a missile has struck this enemy."""
        if not self.is_alive:
            return False

        # Math for collision detection
        dist = math.sqrt((self.x - missile_x)**2 + (self.y - missile_y)**2)

        if dist < (self.radius + missile_radius):
            self.is_alive = False # Requirement: Missile strike destroys enemy
            return True

        return False

    def reached_ground(self, ground_level):
        #Checks if enemy reached the bottom
        if self.is_alive and self.y <= ground_level:
            return True
        return False

    def is_at_edge(self):
        #Checks if the enemy is touching the side of the screen.
        if not self.is_alive:
            return False
        # Buffer to keep them from moving off screen
        return self.x <= 0.05 or self.x >= 0.95

