import time


class Game:

    def __init__(self, screen, snake, food_turtle, scoreboard):
        self.screen = screen
        self.snake = snake
        self.food = food_turtle
        self.scoreboard = scoreboard
        self.points = self.scoreboard.points
        self.game_over = False


    def check_snake_ate_food(self):
        head = self.snake.head
        if head.distance(self.food) <= head.size / 4:
            self.food.move_position()
            self.snake.grow_by_one()
            self.scoreboard.increase_score()
            return True
        

    def has_collided(self):
        if self.snake.hit_wall():
            return True
        if self.snake.hit_self():
            return True
        return False
    

    def run_game(self):
        self.screen.tracer(0)
        self.screen.update()
        
        while not self.game_over:
            self.snake.move_forward()
            self.check_snake_ate_food()

            self.screen.update()
            time.sleep(0.1)

            if self.has_collided():
                self.game_over = True
                self.scoreboard.check_update_high_score()
                self.scoreboard.show_game_over()
        
        self.screen.update()


    def ask_start_new(self):
        try:
            while True:
                response = self.screen.textinput('Game Over', 'Play again? Enter "Y" or "N"\n')
                if response is None:
                    break
                elif response:
                    r = response.lower().strip()
                    if r == 'y':
                        return True
                    elif r == 'n':
                        return False
                
                print('Invalid response. Must be "y" or "n".')
                # raise ValueError('Invalid response. Must be "y" or "n".')
        
        except Exception:
            return