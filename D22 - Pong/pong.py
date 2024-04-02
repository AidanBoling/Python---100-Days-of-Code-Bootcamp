from turtle import RawTurtle

PIXEL_SIZE = 20
AXIS_OFFSET = -5

DOWN = 270 
UP = 90
LEFT = 180 
RIGHT = 0

# [x] detect ball collision with paddle -- (add point to player)
# [x] detect ball off screen 

#Ball mechanics - bounces
    # [x] Starts "on" P1 paddle
    # [x] Goes towards bottom, bounces, angles up to P2
    # [x] If collides with paddle, bounces back -- (plus, increase_score(player))
    # [x] If collides with wall, game over

#TODO: refinement -- change ball bounce_back angle depending on area of paddle it hits...
        # on collision, the greater the ball.distance(paddle), the bounce_back angle changes by +1??
# [x]  refinement -- adjust move speed every time ball hits 
#TODO (maybe): refinement - when ball "on" a paddle, allow ball to move with paddle (so player can change the ball start pos)?
#TODO (maybe): refinement - when a player score updates, only update that score, rather than whole screen (...prob use separate turtles for each -- dash, p1 score, p2 score ?)

#TODO: fix so that player gets point only if other player misses (ball off screen) (instead of off-screen = game over)
# [x]: fix so that ball resets onto paddle of player who got point --> get player number from self.last_paddle_hit.player
#TODO: conditions for game_over?

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
        self.move_speed = 0.03
        self.start_angle = -40
        self.last_paddle_hit = self.p1
        self.start_pos = (self.p1.xcor() + PIXEL_SIZE, AXIS_OFFSET)

        self.goto(self.start_pos)
        self.setheading(self.start_angle)
        self.settiltangle(-self.start_angle)

        self.listening_for_keys()


    def listening_for_keys(self):
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
        if self.is_moving:
            self.forward(PIXEL_SIZE/2)


    def bounce_off(self):
        '''Normal bounce (incident angle == reflection angle)'''       
        dir = self.heading()
        tilt = self.tiltangle()
        self.setheading(-dir)
        self.settiltangle(-tilt)


    def bounce_back(self):
        '''Reflects ball back in opposite direction'''
        dir = self.heading() + 180
        tilt = -dir
        self.setheading(dir)
        self.settiltangle(tilt)
        self.move_speed *= 0.9


    def hit_wall(self):
        '''Detects if ball collides with a wall. Returns False if no collision, otherwise returns the axis parallel to that wall -- "x" or "y".'''
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
        # If in "range" of paddle, within circle w/ diam. = paddle length, 
        # AND x-coord is close to paddle x-track position, i.e. paddle x-coord, then has collided.

        if self.distance(self.p1) <= self.p1.length/2 and self.xcor() <= self.p1.xcor() + PIXEL_SIZE/2:
            self.last_paddle_hit = self.p1
            return True
        if self.distance(self.p2) <= self.p2.length/2 and self.xcor() >= self.p2.xcor() - PIXEL_SIZE/2:
            self.last_paddle_hit = self.p2
            return True
        return False

    def reset_pos(self):
        '''Sets ball "on" to whichever paddle off of which ball last bounced (last_paddle_hit).'''
        paddle = self.last_paddle_hit
        x = paddle.xcor()
        if paddle.player == 1:
            x += PIXEL_SIZE
        if paddle.player == 2:
            x -= PIXEL_SIZE
        self.goto(x, self.start_pos[1])
        self.is_moving = False


class Paddle(Pixel):

    def __init__(self, screen, player):
        super().__init__(screen)
        self.screen = screen
        self.screen_w = self.screen.window_width()
        self.screen_h = self.screen.window_height()
        self.max_y = self.screen_h / 2 - PIXEL_SIZE
        self.max_x = self.screen_w / 2 - 2 * PIXEL_SIZE
        self.length = 5 * PIXEL_SIZE
        self.x_start = AXIS_OFFSET
        self.y_start = AXIS_OFFSET
        self.shapesize(5, 1)
        self.speed(9)
        self.player = player

        self.listening_for_keys()
        self.set_start_pos()

    def listening_for_keys(self):
        if self.player == 1:
            self.screen.onkey(self.move_up, 'w')
            self.screen.onkey(self.move_down, 's')
        if self.player == 2:
            self.screen.onkey(self.move_up, 'Up')
            self.screen.onkey(self.move_down, 'Down')

        self.screen.listen()
        return True
    
    def set_start_pos(self):
        if self.player == 1: 
            self.x_start -= self.max_x     # left side
        if self.player == 2:
            self.x_start += self.max_x     # right side
        
        self.setposition(self.x_start, self.y_start)
    
    def reset_pos(self):
        self.setposition(self.x_start, self.y_start)

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
        self.hideturtle()
        self.shape('square')
        self.shapesize(.5, .5)
        self.color(color)
        self.penup()
        self.speed(0)
        self.screen_h = screen.window_height()
        self.draw_height = self.screen_h - 2 * PIXEL_SIZE
        self.draw_max_y = self.draw_height/2 - PIXEL_SIZE
        self.x_0 = AXIS_OFFSET
        self.player_points = [0, 0]

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
        
        # TODO (?): move number_shapes to separate file.
        number_shapes = {
                '0': {'width': 3, 'moves': {'1': [3, 6, 3, 6], '2': [3, 6, 3, 6]}, 'directions': {'1': [LEFT, DOWN, RIGHT, UP], '2': [RIGHT, DOWN, LEFT, UP]}}, 
                '1': {'width': 1, 'moves': {'1': [7], '2': [7]}, 'directions': {'1': [DOWN], '2': [DOWN]}},
                '2': {'width': 3, 'moves': {'1': [3, 3, 3, 3, 3, 4], '2': [3, 3, 3, 3, 4]}, 'directions': {'1': [LEFT, RIGHT, DOWN, LEFT, DOWN, RIGHT], '2': [RIGHT, DOWN, LEFT, DOWN, RIGHT]}}, 
                '3': {'width': 3, 'moves': {'1': [3, 3, 3, 3, 3, 3, 4], '2': [3, 3, 3, 3, 3, 4]}, 'directions': {'1': [LEFT, RIGHT, DOWN, LEFT, RIGHT, DOWN, LEFT], '2': [RIGHT, DOWN, LEFT, RIGHT, DOWN, LEFT]}},
                '4': {'width': 3, 'moves': {'1': [6, 3, 3, 4], '2': [3, 3, 3, 7]}, 'directions': {'1': [DOWN, UP, LEFT, UP], '2': [DOWN, RIGHT, UP, DOWN]}},
                '5': {'width': 3, 'moves': {'1': [3, 3, 3, 3, 4], '2': [3, 3, 3, 3, 3, 4]}, 'directions': {'1': [LEFT, DOWN, RIGHT, DOWN, LEFT], '2': [RIGHT, LEFT, DOWN, RIGHT, DOWN, LEFT]}},
                '6': {'width': 3, 'moves': {'1': [3, 6, 3, 3, 3], '2': [3, 3, 6, 3, 3, 3]}, 'directions': {'1': [LEFT, DOWN, RIGHT, UP, LEFT], '2': [RIGHT, LEFT, DOWN, RIGHT, UP, LEFT]}},
                '7': {'width': 3, 'moves': {'1': [3, 3, 7], '2': [3, 7]}, 'directions': {'1': [LEFT, RIGHT, DOWN], '2': [RIGHT, DOWN]} },
                '8': {'width': 3, 'moves': {'1': [3, 6, 3, 6, 3, 3], '2': [3, 6, 3, 6, 3, 3]}, 'directions': {'1': [LEFT, DOWN, RIGHT, UP, DOWN, LEFT], '2': [RIGHT, DOWN, LEFT, UP, DOWN, RIGHT]}},
                '9': {'width': 3, 'moves': {'1': [3, 3, 3, 3, 7], '2': [3, 6, 3, 3, 3]}, 'directions': {'1': [LEFT, DOWN, RIGHT, UP, DOWN], '2': [RIGHT, DOWN, UP, LEFT, UP]}},
                }
        
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
            start_x += d_from_center
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
            


    #Scoreboard might also be better as not Turtle extended, but just "class Scoreboard:", arranging "pixel" turtles to draw??
