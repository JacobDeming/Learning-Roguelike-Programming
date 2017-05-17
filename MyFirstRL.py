import libtcodpy as libtcod

# Game settings
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

# Map settings
MAP_WIDTH = 80
MAP_HEIGHT = 45
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

def make_map():
    # Function called to create the map for the game
    global map
    # Fills the map with unblocked tiles
    map = [[Tile(False)
        for y in range(MAP_HEIGHT)]
            for x in range(MAP_WIDTH)]
    
    # Places two pillars onto the map
    map[30][22].blocked = True
    map[30][22].block_sight = True
    map[50][22].blocked = True
    map[50][22].block_sight = True

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