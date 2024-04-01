from turtle import RawTurtle
import random
import time

SEGMENT_SIZE = 20
SNAKE_HEAD_START = (-SEGMENT_SIZE/4, -SEGMENT_SIZE/4)


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


class Scoreboard(RawTurtle):

    def __init__(self, screen, color='white'):
        super().__init__(screen)
        self.hideturtle()
        self.penup()
        self.color(color)
        self.screen_h = screen.window_height()
        self.points = 0


    def increase_score(self):
        self.points += 1


    def show_game_over(self):
        y_step = self.screen_h/8
        self.setposition(0, y_step * 3)
        self.write(f'GAME OVER', False, align='center', font=('Courier', 24, 'normal'))
        
        self.setposition(0, y_step*2)
        self.write(f'Final Score: {self.points}', True, align='center', font=('Courier', 18, 'normal'))

        self.screen.update()


class FoodTurtle(RawTurtle):
    def __init__(self, screen, color='blue'):
        super().__init__(screen)
        self.screen_w = self.screen.window_width()
        self.screen_h = self.screen.window_height()
        self.speed(0)
        self.penup()
        self.shape('circle')
        self.color(color)
        self.shapesize(.5, .5, .5)
        self.move_position()
    
        
    def move_position(self):
        '''Moves food to random new position (x, y).'''
        # new position has to be on coord that matches the possible positions of a segment
        x_step_range = round((self.screen_w / 2 ) / SEGMENT_SIZE)
        y_step_range = round((self.screen_h / 2 ) / SEGMENT_SIZE)

        random_step_x = random.randint(-x_step_range + 1, x_step_range - 1)
        random_step_y = random.randint(-y_step_range + 2, y_step_range - 2)

        x = random_step_x * SEGMENT_SIZE + SNAKE_HEAD_START[0]
        y = random_step_y * SEGMENT_SIZE + SNAKE_HEAD_START[1]
        
        new_pos = (x, y)
        print(f'Generated food position: {new_pos}')

        super().setposition(new_pos)

        # TODO (maybe): new position also can't be on an existing segment (?) -- repeat coord gen until get one that doesn't conflict with existing segment


class Snake:

    def __init__(self, screen, color='white'):
        self.screen = screen
        self.screen_w = self.screen.window_width()
        self.screen_h = self.screen.window_height()
        self.color = color
        self.len_init = 3
        self.start_pos = SNAKE_HEAD_START
        self.segment_size = SEGMENT_SIZE
        self.segments = []
        self.is_moving = False
        self.positions = []
        
        self.create_snake(self.len_init)
        self.head = self.segments[0]
        self.listening_for_keys()


    def create_snake(self, length):
        x = self.start_pos[0]
        y = self.start_pos[1]

        for _ in range(length):
            self.add_segment_at((x, y))
            x -= SEGMENT_SIZE


    def grow_by_one(self):
        last_seg = self.segments[-1]
        pos = last_seg.position()
        self.add_segment_at(pos)


    def add_segment_at(self, position):
        segment = SnakeSegment(screen=self.screen, color=self.color)
        segment.setpos(position)
        self.segments.append(segment)
        # self.positions.append(segment.position())


    def toggle_is_moving(self):
        if self.is_moving == True:
            self.is_moving = False
        else:
            self.is_moving = True
    

    def listening_for_keys(self):
        self.screen.onkey(self.toggle_is_moving, 'space')
        self.screen.onkey(self.turn_up, 'Up')
        self.screen.onkey(self.turn_down, 'Down')
        self.screen.onkey(self.turn_left, 'Left')
        self.screen.onkey(self.turn_right, 'Right')
        self.screen.listen()
        return True


    def move_forward(self):
        if self.is_moving:
            self.move_body()
            self.head.forward_one()
            # self.positions.pop()
            # self.positions.insert(0, self.head.position())


    def move_body(self):
        '''Move each segment to position and direction of the segment in front of it.'''
        range_max = len(self.segments) - 1
        
        for n in range(range_max, 0, -1):
            if n > 0:
                next = self.segments[n-1]
                self.segments[n].goto(next.position())
                self.segments[n].setheading(next.heading())


    def turn_head(self, dir):
        '''Snake turns only if new dir is at right angle to current. No action if would continue forward or turn backwards.'''
        # Uses the heading of the segment just after head, to fix bug where could quickly turn head same direction twice
        # before snake continues moving, so snake ended up going backwards.
        current_dir = int(self.segments[1].heading())
        diff = abs(360 - current_dir - dir)

        if diff == 90 or diff == 270:
            self.head.setheading(dir)


    def turn_up(self):
        self.turn_head(90)


    def turn_down(self):
        self.turn_head(270)


    def turn_left(self):
        self.turn_head(180)


    def turn_right(self):
        self.turn_head(0)


    # Other
    def hit_wall(self):
        pos = self.head.position()
        max_x = (self.screen_w - self.head.size) / 2
        max_y = (self.screen_h - self.head.size) / 2
        
        if pos[0] > max_x or pos[0] < -max_x or pos[1] >= max_y or pos[1] <= -max_y:
            # print(pos)
            return True
        return False
    

    def hit_self(self):
        for segment in self.segments[1:]:
            if self.head.distance(segment.pos()) < self.head.size / 2:
                print('Snake bit itself!')
                return True
        return False
    
    # def hit_self(self):
        # for pos in self.snake.positions[1:]:
        #     if self.head.distance(pos) < head.size / 2:
        #         print('Snake bit itself!')
        #         return True
        # return False


class SnakeSegment(RawTurtle):

    def __init__(self, screen, color):
        super().__init__(screen)
        self.size = SEGMENT_SIZE
        self.shape('square')
        self.penup()
        self.speed(0)
        self.color(color)

    def forward_one(self):
        super().forward(self.size)



#TEMP Archive:
    
    # def snake_bit_self(self):
    #     return self.snake.hit_self()
        # head = self.snake.head
        
        # for pos in self.snake.positions[1:]:
        #     if head.distance(pos) <= head.size / 4:
        #         print('Snake bit itself!')
        #         return True
        # return False