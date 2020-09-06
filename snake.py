class Cube:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color


class SnakeCube(Cube):
    dirs = {1: "Up", 2: "Down", 3: "Left", 4: "Right"}
    current_dir = dirs[4]

    def __init__(self, x, y, width, height, vel, screen_width, screen_height, color, last=False):
        Cube.__init__(self, x, y, width, height, color)
        self.vel = vel
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.last = last

    def move_segment(self):
        if self.current_dir == "Up":
            self.y -= self.vel
        elif self.current_dir == "Down":
            self.y += self.vel
        elif self.current_dir == "Left":
            self.x -= self.vel
        elif self.current_dir == "Right":
            self.x += self.vel
        if self.x > self.screen_width - self.width - self.vel:
            self.x = self.vel
        if self.y > self.screen_height - self.height - self.vel:
            self.y = self.vel
        if self.y < self.vel:
            self.y = self.screen_height - self.vel
        if self.x < self.vel:
            self.x = self.screen_width - self.vel
        
        


class Snake:
    body = []
    anchor = []
    body_lenght = 0
    color = (255, 0, 0)
    hungry = False 
    dead = False

    def __init__(self, start_x, start_y, cube_width, cube_height, vel, sc_width, sc_height):
        self.start_x = start_x
        self.start_y = start_y
        self.cube_width = cube_width
        self.cube_height = cube_height
        self.vel = vel
        self.sc_width = sc_width
        self.sc_height = sc_height
        self.head = SnakeCube(self.start_x, self.start_y, self.cube_width,
                              self.cube_height, self.vel, self.sc_width, self.sc_height, (0, 0, 255))
        #FIRST THREE CUBES OF THE BODY
        self.body.append(self.head)
        self.body.append(SnakeCube(self.start_x - self.cube_width, self.start_y,
                                   self.cube_width, self.cube_height, self.vel, self.sc_width, self.sc_height, self.color))
        self.body.append(SnakeCube(self.start_x - 2*self.cube_width, self.start_y, self.cube_width,
                                   self.cube_height, self.vel, self.sc_width, self.sc_height, self.color, True))
        self.body_lenght += 3
    #TO CREATE THE SNAKE MOVEMENT EFFECT
    def set_dir(self, num):
        self.anchor_x = self.head.x
        self.anchor_y = self.head.y
        break_point = {'anchor_x': self.anchor_x,
                       'anchor_y': self.anchor_y, 'dir': num}
        if not break_point in self.anchor:
            self.anchor.append(break_point)
    #MOVEMENT: SOMETHING CHANGES WHEN:
        # -1: The snake touches its own body --> death
        # -2: The snake eats food --> its body grows
        # -3: A cube of the snake's body encounters an anchor and it has to change direction
    def move(self):
        snake_head = self.body[0]
        for snake_cube in self.body:
            if snake_head.x == snake_cube.x and snake_head.y == snake_cube.y and snake_head != snake_cube:
                self.dead = True
            if snake_cube.x == self.food.x and snake_cube.y == self.food.y:
                self.add_cube()
                self.hungry = False
            for anchor in self.anchor:
                if snake_cube.x == anchor['anchor_x'] and snake_cube.y == anchor['anchor_y']:
                    snake_cube.current_dir = snake_cube.dirs[anchor['dir']]
                    if snake_cube.last == True:
                        self.anchor.remove(anchor)
            snake_cube.move_segment()
    #ADDS A CUBE TO THE SNAKE'S BODY
    def add_cube(self):
        last_cube = self.body[self.body_lenght - 1]
        last_cube.last = False
        if last_cube.current_dir == "Up":
            new_x = last_cube.x
            new_y = last_cube.y + self.cube_height
            new_dir = 1
        elif last_cube.current_dir == "Down":
            new_x = last_cube.x
            new_y = last_cube.y - self.cube_height
            new_dir = 2
        elif last_cube.current_dir == "Left":
            new_x = last_cube.x + self.cube_width
            new_y = last_cube.y
            new_dir = 3
        elif last_cube.current_dir == "Right":
            new_x = last_cube.x - self.cube_width
            new_y = last_cube.y
            new_dir = 4
        new_cube = SnakeCube(new_x, new_y, self.cube_width, self.cube_height,
                             self.vel, self.sc_width, self.sc_height, self.color, True)
        new_cube.current_dir = new_cube.dirs[new_dir]
        self.body.append(new_cube)
        self.body_lenght += 1
    #SPAWN THE FOOD FOR THE SNAKE (IT'S THE SNAKE WHO SPAWNS ITS OWN FOOD)
    def add_food(self, x, y, width, height, color):
        self.food = Cube(x, y, width, height, color)
        self.hungry = True
    
   #RESTART
    def reinitialize(self, start_x, start_y, cube_width, cube_height, vel, sc_width, sc_height):
        self.body = []
        self.anchor = []
        self.body_lenght = 0
        self.hungry = False
        self.dead = False
        self.__init__(start_x, start_y, cube_width, cube_height, vel, sc_width, sc_height)
