import stddraw 
import sys
import stdaudio
import picture 
import threading

class Game: 

    def __init__(object):
        stddraw.setCanvasSize(800, 600)
        stddraw.setXscale(0, 800)   
        stddraw.setYscale(0, 600)

        object.state = "title screen"
        object.game_over_timer = 0
        object.score = 0

        object.title_image = picture.Picture("Title_screen.png")

        object.music_started = False
        #creates game class
        #screen size (need setting, so no hard code)
        #does game states
        #plays music 
        #check version of stddraw im using bc its behaving weirdly ``

    def play_music_loop(object):

        while True:
            stdaudio.playFile("music.wav")

    def start_music(object):
        music_thread = threading.Thread(target=object.play_music_loop, daemon=True)
        music_thread.start()

    def run(object):
        

        while True:
            object.handle_input()
            object.update()
            object.draw()
            stddraw.show(20)
    #handles imput from player 
    #runs the whole time


    #toke me 2 hours to get the musci to loop so i hope it works 

    def handle_input(object):
        
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            
            if key == "q":
                sys.exit()

            if object.state == "title screen":
                if key == " ":
                    object.start_new_game()
            
            elif object.state == "playing":
                if key == "g":
                    object.end_game()

            elif object.state == "game over":
                pass
    #handles input to start, end and quit the game


    def update(object):
        if not object.music_started:
            object.start_music()        
            object.music_started = True
            
        if object.state == "playing":
            pass

        elif object.state == "game over":
            object.game_over_timer -= 1
            if object.game_over_timer <= 0:
                object.state = "title screen"

    def draw(object):
        stddraw.clear()

        if object.state == "title screen":
            object.draw_title_screen()

        elif object.state == "playing":
            object.draw_game()

        elif object.state == "game over":
            object.draw_game()
            object.draw_game_over()

    def draw_title_screen(object):
        stddraw.picture(object.title_image, 400, 300)         

    def draw_game(object):
        stddraw.text(20, 580, "Score: " + str(object.score))
        stddraw.text(400, 300, "Game is running...")


    def draw_game_over(object):
        stddraw.setPenColor(stddraw.RED)
        stddraw.setFontSize(50)
        stddraw.text(400,300, "GAME OVER")
        stddraw.setFontSize(20)
        stddraw.setPenColor(stddraw.BLACK)
        stddraw.text(400, 230, "Final Score: " + str(object.score))
        stddraw.text(400, 200, "Returning to title screen... ")    

    def start_new_game(object):
        object.score = 0
        object.state = "playing"

    def end_game(object):
        object.state = "game over"
        object.game_over_timer = 120
        
my_game = Game()
my_game.run()
