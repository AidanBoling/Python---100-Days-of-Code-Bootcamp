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
    run_game(screen, scoreboard, ball)
    
    screen.exitonclick()


def run_game(screen, scoreboard, ball):
    game_over = False
    screen.tracer(0)
    screen.update()
    
    while not game_over:
        ball.in_play() 
        
        if ball.hit_paddle():
            ball.bounce_back()
            
        hit_wall = ball.hit_wall()
        if hit_wall == 'x':
            ball.bounce_off()
        elif hit_wall == 'y':
            paddle = ball.last_paddle_hit
            player = paddle.player
            print('player scored: ', player)
            scoreboard.increase_score(player)
            ball.reset_pos()
            paddle.reset_pos()
            # game_over = True

        screen.update()
        time.sleep(ball.move_speed)
    
    # Todo: When game over...
    
    screen.update()


def setup_screen(screen, w=1020, h=560, title='Pong'):
        screen.setup(width=w, height=h)
        screen.bgcolor('black')
        screen.title(title)
        screen.tracer(0)

def ball_collision():
    # if ball.distance(paddle)
    pass

main()