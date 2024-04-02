from turtle import Screen
from pong import Ball, Paddle, Scoreboard
import time


def main():
    # Setup

    # continue_play = True
    screen = Screen()
    

    # while continue_play:
    setup_screen(screen)

    paddle1 = Paddle(screen, 1)
    paddle2 = Paddle(screen, 2)
    ball = Ball(screen, paddle1, paddle2)
    scoreboard = Scoreboard(screen)
    screen.update()


    # run_game(screen)
    
    screen.exitonclick()


def run_game(screen):
    game_over = False
    screen.tracer(0)
    screen.update()
    
    while not game_over:
        # ball.move()
        # # self.check_ball_hit_paddle

        screen.update()
        time.sleep(0.1)

        # if self.has_collided():
        #     self.game_over = True
        #     self.scoreboard.show_game_over()
    
    screen.update()


def setup_screen(screen, w=1020, h=560, title='Pong'):
        screen.setup(width=w, height=h)
        screen.bgcolor('black')
        screen.title(title)
        screen.tracer(0)


main()