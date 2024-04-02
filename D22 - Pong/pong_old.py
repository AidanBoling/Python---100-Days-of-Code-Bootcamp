from turtle import RawTurtle
import time

PIXEL_SIZE = 20
AXIS_OFFSET = -5

DOWN = 270 
UP = 90
LEFT = 180 
RIGHT = 0

# [x] detect ball collision with paddle -- (add point to player)
# [x] detect ball off screen -- (game over)

#Ball mechanics - bounces
    # [x] Starts "on" P1 paddle
    # [x] Goes towards bottom, bounces, angles up to P2
    # [x] If collides with paddle, bounces back -- (plus, increase_score(player))
    # [x] If collides with wall, game over

#TODO: refinement -- ball bounce_back should change depending on angle hit by paddle...

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
        self.start_pos = (self.p1.pixels[1].xcor() + PIXEL_SIZE, 0)
        self.is_moving = False
        self.start_angle = -40

        self.goto(self.start_pos)
        self.setheading(self.start_angle)
        self.settiltangle(-self.start_angle)

        self.listening_for_keys()


    def listening_for_keys(self):
        self.screen.onkey(self.toggle_is_moving, 'space')
        # self.screen.onkey(self.in_play, 'Right')

        self.screen.listen()
        return True


    def toggle_is_moving(self):
        if self.is_moving == True:
            self.is_moving = False
        else:
            self.is_moving = True


    def in_play(self):
        if self.is_moving:
            self.forward(PIXEL_SIZE/2)


    def bounce_off(self):       
        dir = self.heading()
        tilt = self.tiltangle()
        self.setheading(-dir)
        self.settiltangle(-tilt)


    def bounce_back(self):
        dir = self.heading() + 180
        tilt = -dir
        self.setheading(dir)
        self.settiltangle(tilt)


    def hit_wall(self):
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
        for pixel in self.p1.pixels:
            if self.distance(pixel) <= PIXEL_SIZE/2:
                return 1
        for pixel in self.p2.pixels:
            if self.distance(pixel) <= PIXEL_SIZE/2:
                return 2
        return False


class Paddle:
    def __init__(self, screen, player):
        self.screen = screen
        self.screen_w = self.screen.window_width()
        self.screen_h = self.screen.window_height()
        self.max_y = self.screen_h / 2 - PIXEL_SIZE
        self.max_x = self.screen_w / 2 - 2 * PIXEL_SIZE
        self.x_start = AXIS_OFFSET
        self.y_start = PIXEL_SIZE + AXIS_OFFSET
        self.pixel_color = 'white'
        self.length = 5
        self.pixels = []
        self.player = player

        self.listening_for_keys()
        self.create_paddle()


    def listening_for_keys(self):
        if self.player == 1:
            self.screen.onkey(self.move_up, 'w')
            self.screen.onkey(self.move_down, 's')
        if self.player == 2:
            self.screen.onkey(self.move_up, 'Up')
            self.screen.onkey(self.move_down, 'Down')

        self.screen.listen()
        return True
    

    def create_paddle(self):
        y = self.y_start
        x = self.x_start

        if self.player == 1: 
            x -= self.max_x     # left side

        if self.player == 2:
            x += self.max_x     # right side

        for _ in range(self.length):
            self.add_pixel_at((x, y))
            y -= PIXEL_SIZE


    def add_pixel_at(self, position):
        pixel = Pixel(screen=self.screen, color=self.pixel_color)
        pixel.setpos(position)
        self.pixels.append(pixel)


    def move(self, pixels, dir):
        leading_pixel = pixels[0]
        leading_pixel.setheading(dir)
        self.move_paddle(pixels, dir)
        leading_pixel.forward_one()


    def move_paddle(self, pixels, dir):
        '''Move each pixel to position and direction of the segment in front of it.'''
        range_max = len(pixels[1::])
        for n in range(range_max, 0, -1):
            if n > 0:
                next = pixels[n-1]
                pixels[n].goto(next.position())


    def move_up(self):
        if self.pixels[0].ycor() < self.max_y - PIXEL_SIZE/2:
            self.move(self.pixels, UP)


    def move_down(self):
        if self.pixels[-1].ycor() > -self.max_y + PIXEL_SIZE:
            self.move(self.pixels[::-1], DOWN)


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
        self.draw_score(player_num)
        
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
