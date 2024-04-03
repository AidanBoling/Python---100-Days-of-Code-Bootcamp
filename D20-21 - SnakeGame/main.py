from turtle import Screen
from snake_game import Game
from snake import Snake
from food import FoodTurtle
from scoreboard import Scoreboard
# import os

# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))

def main():
    continue_play = True
    screen = Screen()

    while continue_play:
        setup_screen(screen)

        snake = Snake(screen)
        food = FoodTurtle(screen)
        scoreboard = Scoreboard(screen)
        
        game = Game(screen, snake, food, scoreboard)

        game.run_game()
        continue_play = game.ask_start_new()
        
        if continue_play:   
            screen.clearscreen()

    screen.exitonclick()


def setup_screen(screen, w=600, h=620, title='Snake Game'):
        screen.setup(width=w, height=h)
        screen.bgcolor('black')
        screen.title(title)
        screen.tracer(0)


main()