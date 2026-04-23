import stddraw

class GameInfo:
    def __init__(self):
        # Updated controls dictionary including the Pause button
        self.controls = {
            "A": "Move LEFT",
            "D": "Move RIGHT",
            "S": "STOP Motion",
            "P": "PAUSE / UNPAUSE",
            "SPACE": "FIRE Cannon",
            "Q": "QUIT Game"
        }

    def draw_instructions(self):
        """
        Draws the key-action pairs on the screen.
        Adjusted colours for high visibility on dark backgrounds.
        """
        stddraw.setFontSize(22)
        current_y = 0.45  # Starting height for the list
        
        for key, action in self.controls.items():
            # Draw the Key in Cyan
            stddraw.setPenColor(stddraw.CYAN)
            stddraw.text(0.4, current_y, f"[{key}]")
            
            # Draw the Action in White
            stddraw.setPenColor(stddraw.WHITE)
            stddraw.text(0.6, current_y, action)
            
            # Move down for the next line
            current_y -= 0.05

    def draw_objective(self):
        """Optional: Draw a small reminder of the goal."""
        stddraw.setPenColor(stddraw.YELLOW)
        stddraw.setFontSize(18)
        stddraw.text(0.5, 0.1, "Objective: Destroy all invaders!")

