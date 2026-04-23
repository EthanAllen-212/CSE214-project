import stddraw
import sys
import shooter
import missile
import enemyfile2
import stdrandom
import threading
from gameinfo import GameInfo # Importing your custom class

# Safe imports for audio/picture
try:
    import picture
except:
    picture = None
try:
    import stdaudio
except:
    stdaudio = None

class Game:
    def __init__(self):
        stddraw.setCanvasSize(800, 600)
        stddraw.setXscale(0.0, 1.0)
        stddraw.setYscale(0.0, 1.0)

        self.enemy_dx = 0.005
        self.enemy_drop = 0.05
        self.state = "title screen"
        self.score = 0
        self.wave = 1
        self.game_over_timer = 120

        self.player = None
        self.enemies = []
        self.missiles = []
        self.info = GameInfo() # Initialise the imported GameInfo
        
        self.title_image = "Title_screen.png"
        self.galaxy_bg = "galaxy.png"
        self.music_started = False

    # ---------------- AUDIO ----------------
    def play_music(self):
        if not stdaudio: return
        try:
            while True: stdaudio.playFile("music.wav")
        except: pass

    def start_music(self):
        if self.music_started: return
        self.music_started = True
        if stdaudio:
            threading.Thread(target=self.play_music, daemon=True).start()

    # ---------------- MAIN LOOP ----------------
    def run(self):
        while True:
            self.start_music()
            self.handle_input()
            self.update()
            self.draw()
            stddraw.show(20)

    # ---------------- INPUT (A, D, S, P) ----------------
    def handle_input(self):
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped().lower()
            
            if key == "q": sys.exit()

            # Pause Toggle
            if key == "p":
                if self.state == "playing": self.state = "paused"
                elif self.state == "paused": self.state = "playing"

            if self.state == "title screen":
                if key == " ": self.start_new_game()
            
            elif self.state == "playing":
                if self.player:
                    self.player.controls(key)
                    if key == " ":
                        m = self.player.shoot()
                        if m: self.missiles.append(m)

    # ---------------- UPDATE ----------------
    def update(self):
        # Freeze game if not in "playing" state
        if self.state != "playing":
            if self.state == "game over":
                self.game_over_timer -= 1
                if self.game_over_timer <= 0: self.state = "title screen"
            return 

        if self.player: self.player.update()
        for m in self.missiles: m.update()

        # Enemy Movement
        hit_edge = False
        for e in self.enemies:
            if e.is_alive and e.is_at_edge():
                hit_edge = True
                break

        if hit_edge:
            self.enemy_dx *= -1
            for e in self.enemies: e.move(self.enemy_dx, -self.enemy_drop)
        else:
            for e in self.enemies: e.move(self.enemy_dx, 0)

        # Missile Collisions
        missile_radius = 0.01
        for m in self.missiles[:]:
            hit = False
            for e in self.enemies:
                if e.is_alive and e.check_collision(m.x, m.y, missile_radius):
                    self.score += 100
                    e.is_alive = False
                    hit = True
                    break
            if hit: self.missiles.remove(m)

        # FAIL CONDITIONS (Touch ship or cross bottom)
        for e in self.enemies:
            if e.is_alive:
                if e.y < 0.12 or (self.player and e.check_collision(self.player.x, self.player.y, 0.05)):
                    self.end_game()

        self.missiles = [m for m in self.missiles if not m.off_screen()]
        
        if len(self.enemies) > 0 and all(not e.is_alive for e in self.enemies):
            self.wave += 1
            self.spawn_wave()

    # ---------------- DRAW ----------------
    def draw(self):
        # No gray background - start with black
        stddraw.clear(stddraw.BLACK)

        # Layer 1: Background Galaxy
        try:
            stddraw.picture(0.5, 0.5, self.galaxy_bg)
        except:
            pass

        # Layer 2: State-specific content
        if self.state == "title screen":
            self.draw_title()
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "paused":
            self.draw_game()
            self.draw_pause_overlay()
        elif self.state == "game over":
            self.draw_game()
            self.draw_game_over()

    def draw_title(self):
        try:
            stddraw.picture(0.5, 0.5, self.title_image)
        except:
            stddraw.setPenColor(stddraw.WHITE)
            stddraw.setFontSize(30)
            stddraw.text(0.5, 0.7, "COSMIC CONQUISTADORS")

        # Instructions from gameinfo class
        self.info.draw_instructions()

        stddraw.setPenColor(stddraw.YELLOW)
        stddraw.setFontSize(20)
        stddraw.text(0.5, 0.15, "PRESS SPACE TO START")

    def draw_game(self):
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.text(0.1, 0.95, "Score: " + str(self.score))
        if self.player: self.player.draw()
        for e in self.enemies: e.draw()
        for m in self.missiles: m.draw()

    def draw_pause_overlay(self):
        stddraw.setPenColor(stddraw.WHITE)
        stddraw.setFontSize(40)
        stddraw.text(0.5, 0.55, "PAUSED")
        stddraw.setFontSize(20)
        stddraw.text(0.5, 0.45, "Press 'P' to Resume")

    def draw_game_over(self):
        stddraw.setPenColor(stddraw.RED)
        stddraw.setFontSize(40)
        stddraw.text(0.5, 0.6, "GAME OVER")

    # ---------------- GAME SETUP ----------------
    def start_new_game(self):
        self.score = 0
        self.state = "playing"
        self.player = shooter.Shooter(0.5, 0.1)
        self.missiles = []
        self.wave = 1
        self.spawn_wave()

    def spawn_wave(self):
        self.enemies = []
        base_speed = 0.005
        self.enemy_dx = base_speed + (self.wave - 1) * 0.0015
        for r in range(3):
            for c in range(5):
                x = 0.2 + c * 0.12
                y = 0.8 - r * 0.12
                self.enemies.append(enemyfile2.Enemy(x, y))

    def end_game(self):
        self.state = "game over"
        self.game_over_timer = 120

if __name__ == "__main__":
    game = Game()
    game.run()

