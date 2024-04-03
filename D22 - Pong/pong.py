from turtle import RawTurtle
from data import number_shapes

PIXEL_SIZE = 20
AXIS_OFFSET = -5

DOWN = 270 
UP = 90
LEFT = 180 
RIGHT = 0

#TODO (maybe): refinement - when ball "on" a paddle, allow ball to move with paddle (so player can change the ball start pos)?
#TODO (maybe): refinement - when a player score updates, only update that score, rather than whole screen (...prob use separate turtles for each -- dash, p1 score, p2 score ?)
#TODO: refinement - at game start, add a message of "press space to start ball moving" (clears when spacebar pressed)
#TODO: conditions for game_over?
#   TODO: refinement - end-of-game messages, etc.
#Check (someday): Paddles move kind of slowly. Limitation of turtle, or something that can be fixed?


class Pixel(RawTurtle):

    def __init__(self, screen, color='white'):
        super().__init__(screen)
        self.size = PIXEL_SIZE
        self.shape('square')
        self.penup()
        self.speed(0)
        self.color(color)


    def forward_one(self):
        self.forward(self.size)


class Ball(Pixel):

    def __init__(self, screen, paddle1, paddle2):
        super().__init__(screen)
        self.screen = screen
        self.p1 = paddle1
        self.p2 = paddle2
        self.bounds_x = self.screen.window_width()/2
        self.bounds_y = self.screen.window_height()/2
        self.x_0 = AXIS_OFFSET
        self.is_moving = False
        self.direction = 'right'
        self.move_speed = 0.03
        self.start_angle = -45
        self.last_paddle_hit = self.p1
        self.start_pos = (self.p1.xcor() + PIXEL_SIZE, AXIS_OFFSET)

        self.goto(self.start_pos)
        self.setheading(self.start_angle)
        self.settiltangle(-self.start_angle)

        self.listening_for_keys()


    def listening_for_keys(self):
        '''Keyboard control -- use spacebar to pause/resume motion of the ball.'''
        self.screen.onkey(self.toggle_is_moving, 'space')
        self.screen.listen()
        return True


    def toggle_is_moving(self):
        '''Toggles whether ball can move forward or not.'''
        if self.is_moving == True:
            self.is_moving = False
        else:
            self.is_moving = True


    def in_play(self):
        '''Ball moves forward, as long as is_moving is True'''
        if self.is_moving:
            self.forward(PIXEL_SIZE/2)


    def bounce_off(self):
        '''Normal bounce (incident angle == reflection angle)'''
        dir = self.heading()
        tilt = self.tiltangle()
        self.setheading(-dir)
        self.settiltangle(-tilt)
        self.set_ball_dir()


    def bounce_back(self):
        '''Reflects ball back in opposite direction.'''
        dir = self.heading() + 180
        tilt = -dir
        self.setheading(dir)
        self.settiltangle(tilt)
        self.set_ball_dir()


    def set_ball_dir(self):
        if 270 > self.heading() > 90: 
            self.direction = 'left'
        else:
            self.direction = 'right'

    
    def paddle_change_heading(self, factor=2):
        '''Changes ball heading slightly depending how far from the center of the paddle the ball hit. Takes a 
        positive number that changes the amount of the direction change. Inverse relationship -- larger numbers 
        will decrease total angle change. Default is 2.'''
        if factor <= 0:
            raise ValueError('Factor must be positive number greater than 0.')
        
        d_heading = self.distance(self.last_paddle_hit)/factor
        if self.xcor() > 0:
            self.setheading(self.heading() + d_heading)
            self.settiltangle(self.tiltangle() - d_heading)
        else:
            self.setheading(self.heading() - d_heading)
            self.settiltangle(self.tiltangle() + d_heading)


    def hit_wall(self):
        '''Detects if ball collides with a wall. Returns False if no collision, otherwise returns the axis parallel 
        to that wall -- "x" or "y".'''
        pos = self.pos()
        left_wall = round(self.x_0 - self.bounds_x + PIXEL_SIZE)
        right_wall = round(self.x_0 + self.bounds_x - PIXEL_SIZE)
        top_wall = round(self.bounds_y - PIXEL_SIZE)
        bottom_wall = round(-self.bounds_y + PIXEL_SIZE)
        
        if pos[0] > right_wall or pos[0] < left_wall:
            return 'y'
        if pos[1] >= top_wall or pos[1] <= bottom_wall:
            return 'x'
        return False
    

    def hit_paddle(self):
        '''Detects whether ball has collided with a paddle. If ball hits a paddle, sets that paddle as last_paddle_hit, 
        ball speed increases, and returns True.'''

        # If ball in "range" of paddle (circle w/ diam. of paddle length), and it's x-coord is 
        # within the "hit" area (1 PIXEL wide) in front of paddle, then ball has collided.
        
        if self.is_moving:
            if self.direction == 'left':   # ball is moving towards left side
                paddle = self.p1
                paddle_range = self.p1.length / 2

            else:
                paddle = self.p2
                paddle_range = self.p2.length / 2

            # if ball in "range" of paddle
            if self.distance(paddle) <= paddle_range:
                ball_absolute_x = abs(self.xcor())
                
                # if ball x-coord is within paddle "hit" zone
                if abs(paddle.hit_boundary_x) <= ball_absolute_x < abs(paddle.surface_x):
                    self.last_paddle_hit = paddle
                    self.move_speed *= 0.9
                    return True            
        
        return False


    def reset_pos(self, paddle=''):
        '''Sets ball "on" paddle indicated, with is_moving = False. Default is paddle 1.'''
        if not paddle:
            paddle = self.p1
        
        if paddle.xcor() > 0:
            self.start_angle *= -1
        
        self.is_moving = False
        self.setheading(self.start_angle)
        self.settiltangle(-self.start_angle)
        self.set_ball_dir()
        self.goto(paddle.hit_boundary_x, self.start_pos[1])


class Paddle(Pixel):

    def __init__(self, screen, player):
        super().__init__(screen)
        self.screen = screen
        self.screen_w = self.screen.window_width()
        self.screen_h = self.screen.window_height()
        self.max_y = self.screen_h / 2 - PIXEL_SIZE
        self.max_x = self.screen_w / 2 - 2 * PIXEL_SIZE
        self.length = 5 * PIXEL_SIZE
        self._surface_x = 0
        self._hit_boundary_x = 0
        self.x_start = AXIS_OFFSET
        self.y_start = AXIS_OFFSET
        self.player = player

        self.shapesize(5, 1)
        self.speed(9)
        self.set_start_pos()
        self.set_surface_x()
        self.set_hit_boundary_x()
        self.listening_for_keys()

    
    def set_start_pos(self):
        if self.player == 1: 
            self.x_start -= self.max_x     # left side
        if self.player == 2:
            self.x_start += self.max_x     # right side
        
        self.setposition(self.x_start, self.y_start)
    

    @property
    def surface_x(self):
        return self._surface_x
    

    @property
    def hit_boundary_x(self):
        return self._hit_boundary_x


    def set_surface_x(self):
        if self.xcor() < 0:
            self._surface_x = self.xcor() + PIXEL_SIZE/2
        else:
            self._surface_x = self.xcor() - PIXEL_SIZE/2


    def set_hit_boundary_x(self):
        if self.xcor() < 0:
            self._hit_boundary_x = self.xcor() + PIXEL_SIZE
        else:
            self._hit_boundary_x = self.xcor() - PIXEL_SIZE
    

    def reset_pos(self):
        self.setposition(self.x_start, self.y_start)


    def listening_for_keys(self):
        if self.player == 1:
            self.screen.onkey(self.move_up, 'w')
            self.screen.onkey(self.move_down, 's')
        if self.player == 2:
            self.screen.onkey(self.move_up, 'Up')
            self.screen.onkey(self.move_down, 'Down')

        self.screen.listen()
        return True
    

    def move(self, dir):
        if dir != int(self.heading()):
            self.setheading(dir)
            self.settiltangle(-dir)
        self.forward_one()


    def move_up(self):
        paddle_top = self.ycor() + self.length / 2
        
        if paddle_top < self.max_y - PIXEL_SIZE/2:
            self.move(UP)


    def move_down(self):
        paddle_bottom = self.ycor() - self.length / 2
        
        if paddle_bottom > -self.max_y + PIXEL_SIZE:
            self.move(DOWN)


class Scoreboard(RawTurtle):

    def __init__(self, screen, color='white'):
        super().__init__(screen)
        self.screen_h = screen.window_height()
        self.draw_height = self.screen_h - 2 * PIXEL_SIZE
        self.draw_max_y = self.draw_height/2 - PIXEL_SIZE
        self.x_0 = AXIS_OFFSET
        self.player_points = [0, 0]
        
        self.hideturtle()
        self.shape('square')
        self.shapesize(.5, .5)
        self.color(color)
        self.penup()
        self.speed(0)
        self.set_field()


    def increase_score(self, player_num):
        self.player_points[player_num - 1] += 1
        
        # Update displayed score 
        self.clearstamps()
        self.set_field()
        
        # TODO: make sure if player_num not int, throws TypeError (pytest)


    def set_field(self):
        # Draw dashed line down middle
        self.shapesize(.25, .75)        
        self.setheading(90)
        self.goto(AXIS_OFFSET, -self.draw_max_y)

        while self.ycor() <= self.draw_height/2:
            self.stamp()
            self.forward((3/2) * PIXEL_SIZE)
        
        self.shapesize(.5, .5)

        # Draw scores
        self.draw_score(player=1)
        self.draw_score(player=2)


    def draw_score(self, player):
        # Numbers "drawn" starting from top-inside corner of score, on each side.
        
        size = PIXEL_SIZE/2
        points = self.player_points[player - 1]
        digits_list = list(str(points))
        d_from_center = 8 * size
        
        start_y = self.draw_max_y
        start_x = self.x_0
        score_digits = []

        if player == 1: 
            start_x -= d_from_center   # left side
            score_digits = digits_list[::-1]

        elif player == 2:
            start_x += d_from_center    # right side
            score_digits = digits_list

        for digit in score_digits:
            shape = number_shapes[digit]
            moves = shape['moves'][f'{player}']
            dir = shape['directions'][f'{player}']

            # Move to start position
            self.goto(start_x, start_y)

            # Print number according to directions
            for i in range(len(dir)):
                self.setheading(dir[i])
                self.stamp_move(moves[i], size)
            
            # Adjust x_position for next number (width of digit, plus spacing)
            d_x = shape['width'] * size + PIXEL_SIZE 
            if player == 2:
                start_x += d_x  
            if player == 1:
                start_x -= d_x


    def stamp_move(self, moves, distance):
        for _ in range(moves):
            self.stamp()
            self.forward(distance)


    # def show_game_over(self):
    #     y_step = self.screen_h/8
    #     self.setposition(0, y_step * 3)
    #     self.write(f'GAME OVER', False, align='center', font=('Courier', 24, 'normal'))
        
    #     self.setposition(0, y_step*2)
    #     self.write(f'Final Score: {self.points}', True, align='center', font=('Courier', 18, 'normal'))

    #     self.screen.update()