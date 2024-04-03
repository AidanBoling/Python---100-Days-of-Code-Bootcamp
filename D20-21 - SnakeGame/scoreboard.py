from turtle import RawTurtle
from pathlib import Path

ROOT_DIR = Path(__file__).parent
HIGH_SCORE_FILE = ROOT_DIR / 'high_score.txt'


class Scoreboard(RawTurtle):

    def __init__(self, screen, color='white'):
        super().__init__(screen)
        self.hideturtle()
        self.penup()
        self.color(color)
        self.screen_h = screen.window_height()
        self.points = 0
        self.high_score = 0
        
        self.get_high_score()
    

    def get_high_score(self):    
        # Try reading the high-score file, create one if doesn't exist
        try:
            with open(HIGH_SCORE_FILE, 'r') as file:
                h_score = file.read()
                self.high_score = int(h_score)

        except FileNotFoundError:
            with open(HIGH_SCORE_FILE, 'x') as file:
                file.write('0')


    def check_update_high_score(self):
        if int(self.points) > int(self.high_score) :
            self.high_score = self.points
            with open(HIGH_SCORE_FILE, 'w') as file:
                file.write(f'{self.points}')


    def increase_score(self):
        self.points += 1


    def show_game_over(self):
        y_step = self.screen_h/8
        self.setposition(0, y_step * 3)
        self.write(f'GAME OVER', False, align='center', font=('Courier', 24, 'normal'))
        
        self.setposition(0, y_step*2)
        self.write(f'Final Score: {self.points}\n\nHigh Score: {self.high_score}', True, align='center', font=('Courier', 18, 'normal'))

        self.screen.update()