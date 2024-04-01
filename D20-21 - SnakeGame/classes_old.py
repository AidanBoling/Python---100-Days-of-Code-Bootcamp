from turtle import Turtle, RawTurtle, Screen
import random



class Game:
    def __init__(self, screen, snake_turtle, food_turtle):
        self.screen = screen
        self.snake = snake_turtle
        self.food = food_turtle
        self.turtles_setup = self.setup_turtles()

    #Game class -- set up screen/canvas; start/stop game methods; track points; set up game logic like snake eat/grow...

    def setup_turtles(self):
        '''Runs on instantiation. Set turtle shapes, sizes, etc.'''
        
        self.snake.shape('square')
        self.snake.shapesize(1, 1/self.snake.size_factor, 1)
        self.snake.penup()
        self.snake.speed(0)
        
        self.food.hideturtle()
        self.food.speed(0)
        self.food.shape('circle')
        self.food.shapesize(.5, .5, .5)
 
        return True

    #     #Snake eat...
    #         # (class Game:) track distance between snake and foodturtle every move of snake; 
    #             #when distance == 0, snake "eats" food --> foodturtle.erasestamp(foodstamp), then new random stamp


    #     # Snake Grow: 
    #         #when eats food, move_forward(1), then keep_moving()
    #     def eat_food():
    #         pass


    #     #Game start:
                
    #     #Start: go a few moves without clearing stamps, then do move_forward()

    #     # Setup -- Create snake length:
    #     #move_forward(snake_length_init)

    #     #Game start:
    #     #keep_moving()

    #     #screen.exitonclick()


    


class FoodTurtle(RawTurtle):
    def __init__(self, canvas):
        self.screen = canvas

        # self.is_styled = self.set_style()
        self.stamp_current = ''
        # self.position_at = (0,0)

        super().__init__(canvas)

    # def set_style(self):
    #     super().hideturtle()
    #     super().speed(0)
    #     super().shape("circle")
    #     super().shapesize(.5, .5, .5)
    #     return True
        
    #makes stamp at random_coord (x, y)-- choose randint() for each x, y, between +/- screen/2, --> set pos, then stamp
    def move_position(self):
        coord_range = self.screen.screensize() / 2
        random_coord = (random.randint(-coord_range, coord_range), random.randint(-coord_range, coord_range))
        # print(random_coord)
        super().goto(random_coord)


    def drop_food(self):
        self.move_position()
        self.stamp_current = super().stamp()


class Snake(RawTurtle):
    # Handles styling; Keeps track of it's own motion; 
    def __init__(self, canvas):
        self.screen = canvas
        self.stamp_size = 5
        self.size_factor = 20 / self.stamp_size
        self.length_init = 3

        self.is_moving = True
        self._key_is_pressed = False #use different var?
        # self._is_styled = self.set_style()
        self._listening_for_keys = self.listening_for_keys()

        super().__init__(canvas)


    # def set_style(self):
    #     super().shape('square')
    #     super().shapesize(1, 1/self.size_factor, 1)
    #     super().penup()
    #     super().speed(0)
    
    
    #Snake Motion:
        # continuous motion
        # snake turns on key press (event listener)

    def listening_for_keys(self):
        self.screen.onkey(self.toggle_snake_motion, 'space') # --> Temp. Probably move to game class, or remove once have game_over functionality set up

        self.screen.onkey(self.turn_up, 'Up')
        self.screen.onkey(self.turn_down, 'Down')
        self.screen.onkey(self.turn_left, 'Left')
        self.screen.onkey(self.turn_right, 'Right')

        self.screen.listen()

        return True

    
    def toggle_snake_motion(self):
        # Note -- need to refactor this, for class format...?
        if not self.is_moving:
            self.is_moving = True
            self.keep_moving()
        else:
            self.is_moving = False


    def keep_moving(self):
        while self.is_moving and not self._key_is_pressed:
            self.move_forward_and_clear()


    # -- Forward
            
    def forward_one(self):
        super().forward(self.stamp_size)
        super().stamp()


    def move_forward(self, n):
        n *= self.size_factor
        while n >= 0:
            self.forward_one()
            n -= 1


    def move_forward_and_clear(self):
        '''Move forward and maintain length of snake -- clears a stamp for each new stamp (move) it makes.'''
        n = self.size_factor
        while n >= 0:
            self.forward_one()
            super().clearstamps(1)
            n -= 1
    

    # -- Turn:
            
    def turn(self, dir):
        '''Snake turns only if new dir is at right angle to current. No action if would continue forward or turn backwards.'''
        current_dir = int(super().heading())
        diff = abs(360 - current_dir - dir)

        if diff == 90 or diff == 270:
            self._key_is_pressed = True
            if self.size_factor > 1:
                position_adjust = (self.stamp_size * self.size_factor - self.stamp_size)/2
                super().back(position_adjust)
                super().setheading(dir)
                super().forward(self.stamp_size * (self.size_factor/2 - 1))
                # snake.forward(position_adjust)
            else:
                super().setheading(dir)
            
            self._key_is_pressed = False
            self.keep_moving()

    def turn_up(self):
        self.turn(90)

    def turn_down(self):
        self.turn(270)

    def turn_left(self):
        self.turn(180)

    def turn_right(self):
        self.turn(0)


    # Distance
        
    def hit_wall(self):
        d_home = super().distance(0, 0) 
        max_d = self.screen.screensize() / 2

        if d_home >= max_d:
            return True
        


#Snake dies (hits wall, hits itself)
    #self.hit_wall = hit_wall()
    #self.hit_self = hit_self()
    #hit_wall(): if snake distance (from home) >= screen_size / 2 --> return True
        
    #hit_self():


#...game play continues While not hit_wall and not hit_self
