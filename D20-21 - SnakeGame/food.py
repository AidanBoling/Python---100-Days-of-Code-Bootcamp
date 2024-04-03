from turtle import RawTurtle
import random

SEGMENT_SIZE = 20
SNAKE_HEAD_START = (-SEGMENT_SIZE/4, -SEGMENT_SIZE/4)


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
        # print(f'Generated food position: {new_pos}')

        super().setposition(new_pos)

        # TODO (maybe): refinement - new position also can't be on an existing segment (?) -- repeat coord gen until get one that doesn't conflict with existing segment

