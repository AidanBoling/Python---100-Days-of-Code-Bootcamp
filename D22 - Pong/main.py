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
        
        player_scored = ball.hit_paddle()
        if player_scored:
            ball.bounce_back()
            scoreboard.increase_score(player_scored)

        hit_wall = ball.hit_wall()
        if hit_wall == 'x':
            ball.bounce_off()
        elif hit_wall == 'y':
            # ball.bounce_back()
            game_over = True

        screen.update()
        time.sleep(0.05)
    
        # if self.has_collided():
        #     self.game_over = True
        #     self.scoreboard.show_game_over()
    
    screen.update()


def setup_screen(screen, w=1020, h=560, title='Pong'):
        screen.setup(width=w, height=h)
        screen.bgcolor('black')
        screen.title(title)
        screen.tracer(0)

def ball_collision():
    # if ball.distance(paddle)
    pass



    # def check_snake_ate_food(self):
    #     head = self.snake.head
    #     if head.distance(self.food) <= head.size / 4:
    #         self.food.move_position()
    #         self.snake.grow_by_one()
    #         self.scoreboard.increase_score()
    #         return True
        

# def hit_bounce_surface(ball):
    
#     if ball.hit_paddle():
#         return True
#     return False

main()