from game import game 

def main():
    game = game()
    game.run()
    while game_is_running:
        if current_state == "PLAYING":
            game.update() 
            game.draw()

if __name__ == "__main__":    main()    
