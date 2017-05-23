import libtcodpy as libtcod

# Game settings
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

# Map settings
MAP_WIDTH = 80
MAP_HEIGHT = 45
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
color_dark_wall = libtcod.Color(255,255,255)
color_dark_ground = libtcod.Color(0,0,0)

class Tile:
    # A tile of the map and its properties
    def __init__(self,blocked,block_sight = None):
        self.blocked = blocked
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class GameObject:
    # Generic object which can represent anything on the screen
    # Is always represented as a character on screen
    def __init__(self,x,y,char,color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
    def move(self,dx,dy):
        # Move the player by the passed amount so long as the destination is not blocked
        if not map[self.x+dx][self.y+dy].blocked:
            self.x += dx
            self.y += dy
    def draw(self):
        # Set the color of the GameObject and then draw the character that represents this object at a position
        libtcod.console_set_default_foreground(console, self.color)
        libtcod.console_put_char(console,self.x,self.y,self.char,libtcod.BKGND_NONE)
    def clear(self):
        # Erase the character that represents this object
        libtcod.console_put_char(console,self.x,self.y,' ',libtcod.BKGND_NONE)

class Rect:
    # A rectangle on the map which is used to represent a room
    def __init__(self,x,y,w,h):
        self.x1 = x
        self.y1 = y
        self.x2 = x+w
        self.y2 = y+h
    def center(self):
        center_x = (self.x1 + self.x2)/2
        center_y = (self.y1 + self.y2)/2
        return (center_x, center_y)
    def intersect(self,other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

def create_room(room):
    global map
    # Goes through the tiles in the rectangles and makes them passable
    for x in range(room.x1+1,room.x2):
        for y in range(room.y1+1,room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False

def create_h_tunnel(x1,x2,y):
    # Creates a horizontal tunnel between rooms
    global map
    for x in range(min(x1,x2),max(x1,x2)+1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def create_v_tunnel(y1,y2,x):
    # Creates a vertical tunnel between rooms
    global map
    for y in range(min(y1,y2),max(y1,y2)+1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def make_map():
    # Function called to create the map for the game
    global map
    rooms = []
    num_rooms = 0
    # Fills the map with unblocked tiles
    map = [[Tile(True)
        for y in range(MAP_HEIGHT)]
            for x in range(MAP_WIDTH)]
    for r in range(MAX_ROOMS):
        # Random width and height
        w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        # Random position without going out of the boundaries of the map
        x = libtcod.random_get_int(0,0,MAP_WIDTH-w-1)
        y = libtcod.random_get_int(0,0,MAP_HEIGHT-h-1)
        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x,y,w,h)
        # Run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        if not failed:
            # This means there are no intersections, so this room is valid and is painted to the console
            create_room(new_room)
            # Center coordinates of new room, will be useful later
            (new_x,new_y) = new_room.center()
            # This is the first room where the player starts
            if num_rooms == 0:
                player.x = new_x
                player.y = new_y
            else:
                # All rooms after the first: Connect to the previous room with a tunnel
                (prev_x,prev_y) = rooms[num_rooms-1].center()
                if libtcod.random_get_int(0,0,1) == 1:
                    # First move horizontally, then vertically
                    create_h_tunnel(prev_x,new_x,prev_y)
                    create_v_tunnel(prev_y,new_y,new_x)
                else:
                    # First move vertically, then horizontally
                    create_v_tunnel(prev_y,new_y,prev_x)
                    create_h_tunnel(prev_x,new_x,new_y)
            # Append the new room to the list
            rooms.append(new_room)
            num_rooms+=1
        
    

def render_all():
    # Draws all objects in the list
    for object in objects:
        object.draw()
    # Goes through all of the tiles and sets their background color
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                libtcod.console_set_char_background(console,x,y,color_dark_wall,libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(console,x,y,color_dark_ground,libtcod.BKGND_SET)
    # Blit the contents of the "console" to the root console
    libtcod.console_blit(console,0,0,SCREEN_WIDTH,SCREEN_HEIGHT,0,0,0)

def handle_keys():
    key = libtcod.console_check_for_keypress()

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: Toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return True #Escape: Exits the game
    # Movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0,-1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0,1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1,0)
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1,0)

#################
# Initialization and main loop
#################
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'My First Roguelike', False)
console = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
libtcod.sys_set_fps(LIMIT_FPS)
# Creates the player
player = GameObject(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,'@',libtcod.white)

# Creates an npc
npc = GameObject(SCREEN_WIDTH/2-5,SCREEN_HEIGHT/2,'@',libtcod.yellow)
# The list objects that will be placed on the map
objects = [npc,player]
# Generates the map
make_map()

while not libtcod.console_is_window_closed():
    # Draw everything to the screen
    render_all()
    libtcod.console_flush()
    # Erase all objects at their old location before they move
    for object in objects:
        object.clear()
    # Handle key presses and exit the game if needed
    exit = handle_keys()
    if exit:
        break