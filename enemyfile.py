#Rakotsoana Tlotliso 29002877

import stddraw
import math


class Enemy:
    def __init__(self, x, y):
        self.x = x   #position x, y
        self.y = y
        self.radius = 0.025
        self.is_alive = True    #enemy alive,active

    def move(self, dx, dy):   #this changes (x,y) to move enemy across the screen
        self.x += dx
        self.y += dy

    def draw(self):
        if not self.is_alive:    #check if enemy is alive
            return

        stddraw.setPenColor(stddraw.RED)         #how the enemy looks
        stddraw.filledCircle(self.x, self.y, self.radius)

        stddraw.setPenColor(stddraw.BLACK)
        stddraw.filledCircle(self.x, self.y, 0.01)

    def kill(self):
        self.is_alive = False

    def check_collision(self, missile_x, missile_y, missile_radius):  #diist between enemy and bulet
        if not self.is_alive:      #if enemy dead, return
            return False

        dist = math.sqrt((self.x - missile_x)**2 + (self.y - missile_y)**2)  

        if dist < (self.radius + missile_radius):
            self.kill()
            return True

        return False
