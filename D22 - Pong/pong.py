from turtle import RawTurtle

SEGMENT_SIZE = 20
# detect ball collision with paddle -- (add point to player)
# detect ball off screen -- (game over)

#Ball mechanics - bounces
    # Starts "on" P1 paddle
    # Goes towards bottom, bounces, angles up to P2
    # If collides with paddle, bounces back -- (plus, increase_score(player))
    # If collides with wall, game over


class Pixel(RawTurtle):

    def __init__(self, screen, color='white'):
        super().__init__(screen)
        self.size = SEGMENT_SIZE
        self.shape('square')
        self.penup()
        self.speed(0)
        self.color(color)

    def forward_one(self):
        self.forward(self.size)


class Ball(Pixel):
    def __init__(self, screen):
        # super().__init__(screen)
        self.screen = screen
        self.is_moving = False
        self.ball = ''
        
        self.create_ball()
        self.listening_for_keys()

    def listening_for_keys(self):
        self.screen.onkey(self.toggle_is_moving, 'space')
        self.screen.listen()
        return True

    def create_ball(self):
        ball = Pixel(self.screen)
        #set initial position
        self.ball = ball


    def toggle_is_moving(self):
        if self.is_moving == True:
            self.is_moving = False
        else:
            self.is_moving = True


class Paddle:
    def __init__(self, screen, player):
        self.screen = screen
        self.screen_w = self.screen.window_width()
        self.screen_h = self.screen.window_height()
        self.x_start = -self.screen_w/2 + SEGMENT_SIZE*2
        self.y_start = SEGMENT_SIZE
        self.pixel_color = 'white'
        self.length = 3
        self.pixels = []
        self.player = player

        self.listening_for_keys()
        self.create_paddle()

    def listening_for_keys(self):
        self.screen.onkey(self.move_up, 'Up')
        self.screen.onkey(self.move_down, 'Down')
        self.screen.listen()
        return True
    
    def create_paddle(self):
        x = self.x_start
        y = self.y_start

        if self.player == 1: 
            x -= SEGMENT_SIZE/4

        if self.player == 2:
            x *= -1    #right side
            x -= SEGMENT_SIZE/4

        for _ in range(self.length):
            self.add_pixel_at((x, y))
            y -= SEGMENT_SIZE
            # self.add_pixel_at((0,0))

    def add_pixel_at(self, position):
        pixel = Pixel(screen=self.screen, color=self.pixel_color)
        pixel.setpos(position)
        self.pixels.append(pixel)

    def move(self):
        pass


    #  TODO: These were taken from snake game; fix/adapt for pong paddle

    # def move_forward(self):
    #     if self.is_moving:
    #         self.move_body()
    #         self.head.forward_one()

    # def move_body(self):
    #     '''Move each pixel to position and direction of the segment in front of it.'''
    #     range_max = len(self.pixels) - 1
        
    #     for n in range(range_max, 0, -1):
    #         if n > 0:
    #             next = self.segments[n-1]
    #             self.pixels[n].goto(next.position())
    #             self.pixels[n].setheading(next.heading())


    def move_up(self):
        # --> head would be the segment at top --> set self.head = self.pixels[0] ???
        # self.head.setheading(90)
        pass

    def move_down(self):
        # --> head would be the segment at bottom --> set self.head = self.pixels[-1] ???
        # self.head.setheading(270)
        pass
    
    # Can't move past top or bottom of screen




#This might also be better as not Turtle extended, but just "class Scoreboard:", arranging "pixel" turtles to draw:
class Scoreboard(RawTurtle):

    def __init__(self, screen, color='white'):
        super().__init__(screen)
        self.hideturtle()
        self.shape('square')
        self.penup()
        self.color(color)
        self.speed(0)
        self.screen_h = screen.window_height()
        self.draw_height = self.screen_h - 2 * SEGMENT_SIZE
        self.player_points = [0, 0]

        # self.increase_score(1)
        self.set_field()

    def increase_score(self, player_num):
        # Todo: make sure if player_num not int, throws TypeError (pytest)

        self.player_points[player_num] += 1
        # print('points: ', self.player_points[player_num])
        #update shown score 
        self.draw_score(self.player_points[player_num], player_num)


    def set_field(self):
        # Draw dashed line down middle
        self.shapesize(.25, .75, 1)        
        self.setheading(90)

        y = -self.draw_height/2 + SEGMENT_SIZE
        self.goto(0, y)

        while self.ycor() < self.draw_height/2:
            self.stamp()
            self.forward((3/2)*SEGMENT_SIZE)
            
        print(self.pos())
        self.shapesize(1,1,1)

        #draw score_player_1 on left side top
        #draw score_player_2 on right side top

    def draw_score(self, points, player):
        # Move to start position, based on which player
        # start position_x at center + segment_size -> x = -SEGMENT_SIZE; position_y at top -> y = draw_height/2?
        
        # Need to define shapes -- draw path of turtle for numbers ?
        # list dictionary --> numbers = [{'moves': 1, }]
        # array, in order, select by -> numbers[points  - 1]

        #   Split points number into list, iterate through draw process for each number, in reverse order
        #   How to determine start position for each number per score?
        #       ...Start with last digit, then start for next number will be current start + digit width + segment_size 
        
        # for num in score_nums:
        # 

        pass

    # def show_game_over(self):
    #     y_step = self.screen_h/8
    #     self.setposition(0, y_step * 3)
    #     self.write(f'GAME OVER', False, align='center', font=('Courier', 24, 'normal'))
        
    #     self.setposition(0, y_step*2)
    #     self.write(f'Final Score: {self.points}', True, align='center', font=('Courier', 18, 'normal'))

    #     self.screen.update()