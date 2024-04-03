from turtle import RawTurtle

SEGMENT_SIZE = 20
SNAKE_HEAD_START = (-SEGMENT_SIZE/4, -SEGMENT_SIZE/4)


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


    # Collisions
        
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
                # print('Snake bit itself!')
                return True
        return False


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