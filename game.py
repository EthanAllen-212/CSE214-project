import stddraw 
import sys
import stdaudio
import picture 
import threading
import shooter
import missile
import enemyfile2
import stdrandom

class Game: 

    def __init__(self):
        stddraw.setCanvasSize(800, 600)

        self.enemy_dx = 0.005   # How fast they move left/right
        self.enemy_drop = 0.05
        
        self.state = "title screen"
        self.game_over_timer = 0
        self.score = 0

        self.title_image = picture.Picture("Title_screen.png")

        self.music_started = False

        self.player = None
        self.enemies = []
        self.missiles = []
        #creates game class
        #screen size (need setting, so no hard code)
        #does game states
        #plays music 
        #check version of stddraw im using bc its behaving weirdly ``

    def play_music_loop(self):

        while True:
            stdaudio.playFile("music.wav")

    def start_music(self):
        music_thread = threading.Thread(target=self.play_music_loop, daemon=True)
        music_thread.start()

    def run(self):
        

        while True:
            self.handle_input()
            self.update()
            self.draw()
            stddraw.show(20)
    #handles imput from player 
    #runs the whole time


    #toke me 2 hours to get the musci to loop so i hope it works 

    def handle_input(self):
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            
            if key == "q":
                sys.exit()

            if self.state == "title screen":
                if key == " ":
                    self.start_new_game()
            
            elif self.state == "playing":
                if key == "g":
                    self.end_game()

                
                if self.player != None:
                    self.player.controls(key)

                    if key == " ":
                        new_missile = self.player.shoot()
                        if new_missile != None: 
                            self.missiles.append(new_missile)

            elif self.state == "game over":
                pass
    #handles input to start, end and quit the game


    def update(self):
        if not self.music_started:
            self.start_music()        
            self.music_started = True
            
        if self.state == "playing":
            if self.player != None:
                self.player.update()
                
            for m in self.missiles:
                m.update() 

           
            hit_edge = False
            for enemy in self.enemies:
                if enemy.is_alive and enemy.is_at_edge():
                    hit_edge = True
                    break 
            

            if hit_edge:
                self.enemy_dx *= -1 
                for enemy in self.enemies:
                    
                    enemy.move(self.enemy_dx, -self.enemy_drop) 
            else:
                
                for enemy in self.enemies:
                    enemy.move(self.enemy_dx, 0)
            #when enemy hits edge, move down and reverse direction, otherwise just move in current direction
            
            
            missile_radius = 0.01 
            for m in self.missiles[:]:
                hit_something = False
                for enemy in self.enemies:
                    if enemy.is_alive and enemy.check_collision(m.x, m.y, missile_radius):
                        self.score += 100
                        hit_something = True
                        break 
                
                
                if hit_something:
                    self.missiles.remove(m)
                    
            
            for enemy in self.enemies:
                if enemy.is_alive and enemy.reached_ground(0.15):
                    self.end_game()

           
            self.missiles = [m for m in self.missiles if not m.off_screen()]

            for enemy in self.enemies:
                
                pass 
                
            
            self.missiles = [m for m in self.missiles if not m.off_screen()]
        
            any_alive = False
            for enemy in self.enemies:
                if enemy.is_alive:
                    any_alive = True
                    break 
            
           
            if not any_alive:
                self.wave += 1
                self.spawn_wave()
                self.missiles = [] 

        elif self.state == "game over":
            self.game_over_timer -= 1
            if self.game_over_timer <= 0:
                self.state = "title screen"

    def draw(self):
        stddraw.clear()

        if self.state == "title screen":
            self.draw_title_screen()

        elif self.state == "playing":
            self.draw_game()

        elif self.state == "game over":
            self.draw_game()
            self.draw_game_over()

    def draw_title_screen(self):
        stddraw.picture(self.title_image, 0.5, 0.5)         

    def draw_game(self):
        stddraw.text(0.1, 0.95, "Score: " + str(self.score))
        
        if self.player != None:
            self.player.draw()

        for enemy in self.enemies:
            enemy.draw()

        for m in self.missiles:
            m.draw()


    def draw_game_over(self):
        stddraw.setPenColor(stddraw.RED)
        stddraw.setFontSize(50)
        stddraw.text(0.5,0.6, "GAME OVER")
        stddraw.setFontSize(20) 
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.text(0.5, 0.45, "Final Score: " + str(self.score))
        stddraw.text(0.5, 0.35, "Returning to title screen... ")    

    def start_new_game(self):
        self.score = 0
        self.state = "playing"
        self.player = shooter.Shooter(0.5, 0.1) 
        self.missiles = []
        self.enemies = []
        self.enemy_dx = 0.005 
        self.enemies = []
        
        self.wave = 1
        self.spawn_wave()
    
    def spawn_wave(self):
        self.enemies = []
        
        
        base_speed = 0.005
        speed_boost = (self.wave - 1) * 0.0015
        self.enemy_dx = base_speed + speed_boost
        #increase speed each wave
        
        if self.wave == 1:
            
            for row in range(3):
                for col in range(5):
                    x = 0.2 + (col * 0.12)
                    y = 0.8 - (row * 0.12)
                    self.enemies.append(enemyfile2.Enemy(x, y))

        
        else:
            
            max_rows = min(6, 1 + (self.wave // 2)) 
            max_cols = 7
            
            for row in range(max_rows):
                for col in range(max_cols):
                    
                    if stdrandom.bernoulli(0.7): 
                        x = 0.15 + (col * 0.1)
                        y = 0.9 - (row * 0.1)
                        self.enemies.append(enemyfile2.Enemy(x, y))
    #after wave 1 spawn random formations with increasing speed

    def end_game(self):
        self.state = "game over"
        self.game_over_timer = 120
        
my_game = Game()
my_game.run()
