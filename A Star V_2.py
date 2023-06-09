import pygame
from warnings import warn
import heapq
from pygame import *
import random

pygame.init()
fps = 500
fps_clock = pygame.time.Clock()

screen = pygame.display.set_mode((1366, 768))
pygame.display.set_caption("A* Path Finding Visualizer")
icon_image = pygame.image.load('./Assets/path.png')
pygame.display.set_icon(icon_image)

rows, cols = (57, 122)
rect_width = 10
rect_height = 10
start_box_pos = (40, 80)
end_box_pos = (150, 80)
blockers_box_pos = (260, 80)
start_algo_btn_pos = (410, 80)
maze_btn_pos = (530, 80)
clear_paths_btn_pos = (800, 80)
dijkstras_algo_btn_pos = (680, 80)
reset_btn_pos = (1220, 80)

box_arrays = []
animation_list = []
path = []
maze = []

node_list_complete = False
path_list_complete = False

running = True
mouse_motion = False
start_btn_state = False
end_btn_state = False
blockers_btn_state = False
start_algo_btn_state = False
start_btn_clicked = False
end_btn_clicked = False
blockers_btn_clicked = False
animation_completion = False
no_path_found_state = False
maze_created = False
animation_started = False
draw_maze = False
normal_flow = True
clear_paths = False
dijkstras_btn_clickable = False

start_node_position = ()
end_node_position = ()

# Colors Defined
white = pygame.Color(255, 255, 255)
little_off_white = pygame.Color(255, 255, 255, 5)
off_white = pygame.Color(189, 188, 187)
black = pygame.Color(0, 0, 0)
orange_col = pygame.Color(250, 161, 27)
orange_dark_col = pygame.Color(201, 99, 4)
grey_col = pygame.Color('#3FA796')
hinged_sky_blue_col = pygame.Color(255, 140, 26)
start_green_col = pygame.Color(6, 204, 72)
start_green_dark_col = pygame.Color(0, 102, 34)
start_algo_light_col = pygame.Color(5, 143, 242)
start_algo_dark_col = pygame.Color(5, 93, 176)
block_rect_color = black
background_color = pygame.Color("#361d32")
title_color = pygame.Color('#f55951')
box_background_color = pygame.Color(190, 190, 190)
current_node_fill_color = pygame.Color("#FFD93D")
open_list_node_fill_color = pygame.Color("#21ABA5")
clear_path_color = pygame.Color("#FFCC00")
generate_maze_btn_color = pygame.Color("#8495D0")

# Fonts Defined
font_large = pygame.font.Font('./Assets/Roboto-Bold.ttf', 30)
font_medium = pygame.font.Font('./Assets/Roboto-Medium.ttf', 28)
font_small = pygame.font.Font('./Assets/Roboto-Regular.ttf', 16)

def generate_maze():
    # Find number of surrounding cells
    def surroundingCells(rand_wall):
        s_cells = 0
        if (maze[rand_wall[0]-1][rand_wall[1]] == 'c'):
            s_cells += 1
        if (maze[rand_wall[0]+1][rand_wall[1]] == 'c'):
            s_cells += 1
        if (maze[rand_wall[0]][rand_wall[1]-1] == 'c'):
            s_cells +=1
        if (maze[rand_wall[0]][rand_wall[1]+1] == 'c'):
            s_cells += 1

        return s_cells

    ## Main code
    # Init variables
    wall = 'w'
    cell = 'c'
    unvisited = 'u'
    height = 57
    width = 122
    maze = []

    # Initialize colorama

    # Denote all cells as unvisited
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(unvisited)
        maze.append(line)

    # Randomize starting point and set it a cell
    starting_height = int(random.random()*height)
    starting_width = int(random.random()*width)
    if (starting_height == 0):
        starting_height += 1
    if (starting_height == height-1):
        starting_height -= 1
    if (starting_width == 0):
        starting_width += 1
    if (starting_width == width-1):
        starting_width -= 1

    # Mark it as cell and add surrounding walls to the list
    maze[starting_height][starting_width] = cell
    walls = []
    walls.append([starting_height - 1, starting_width])
    walls.append([starting_height, starting_width - 1])
    walls.append([starting_height, starting_width + 1])
    walls.append([starting_height + 1, starting_width])

    # Denote walls in maze
    maze[starting_height-1][starting_width] = 'w'
    maze[starting_height][starting_width - 1] = 'w'
    maze[starting_height][starting_width + 1] = 'w'
    maze[starting_height + 1][starting_width] = 'w'

    while (walls):
        # Pick a random wall
        rand_wall = walls[int(random.random()*len(walls))-1]

        # Check if it is a left wall
        if (rand_wall[1] != 0):
            if (maze[rand_wall[0]][rand_wall[1]-1] == 'u' and maze[rand_wall[0]][rand_wall[1]+1] == 'c'):
                # Find the number of surrounding cells
                s_cells = surroundingCells(rand_wall)

                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])


                    # Bottom cell
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):	
                        if (maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])
                

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Check if it is an upper wall
        if (rand_wall[0] != 0):
            if (maze[rand_wall[0]-1][rand_wall[1]] == 'u' and maze[rand_wall[0]+1][rand_wall[1]] == 'c'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])

                    # Rightmost cell
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Check the bottom wall
        if (rand_wall[0] != height-1):
            if (maze[rand_wall[0]+1][rand_wall[1]] == 'u' and maze[rand_wall[0]-1][rand_wall[1]] == 'c'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)


                continue

        # Check the right wall
        if (rand_wall[1] != width-1):
            if (maze[rand_wall[0]][rand_wall[1]+1] == 'u' and maze[rand_wall[0]][rand_wall[1]-1] == 'c'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if (rand_wall[0] != 0):	
                        if (maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Delete the wall from the list anyway
        for wall in walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                walls.remove(wall)
        
    # Mark the remaining unvisited cells as walls
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == 'u'):
                maze[i][j] = 'w'

    # Set entrance and exit
    for i in range(0, width):
        if (maze[1][i] == 'c'):
            maze[0][i] = 'c'
            break

    for i in range(width-1, 0, -1):
        if (maze[height-2][i] == 'c'):
            maze[height-1][i] = 'c'
            break

    new_maze = [[0 for i in range(width)] for j in range(height)]
    for i in range(0, height):
        for j in range(0, width):
            if maze[i][j] == 'w':
                new_maze[i][j] = 1
    return new_maze

class Node():
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        self.id = -1

        # blank block
        # node_type defines 'blockers', 'free way', 'start node' , 'end node'
        self.node_type = 69

        self.xdist_position = -1
        self.ydist_position = -1

        self.in_open_list = False
        self.in_close_list = False

    def set_positional_index(self, index):
        x_pos, y_pos = index
        self.position = (x_pos, y_pos)

    def set_position(self, x_pos, y_pos):
        self.xdist_position = x_pos
        self.ydist_position = y_pos

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path

box_node_array = [[Node() for i in range(cols)] for j in range(rows)]

# Place the Visualizer billboard at the top of the display window
def draw_text():
    textual_surface = font_large.render("A* Pathfinding Algorithm Visualizer", True, title_color)
    screen.blit(textual_surface, (screen.get_width() / 2 - textual_surface.get_width() / 2, 15))

# Draw the grid base 
def draw_rects():
    global box_arrays
    l_x = 13
    l_y = 131
    outer_shell_rect = (9, 127, 1349, 634)
    pygame.draw.rect(screen, white, outer_shell_rect, width = 4, border_radius = 3)
    for i in range(rows):
        for j in range(cols):
            box_arrays.append((l_x, l_y))
            pygame.draw.rect(screen, little_off_white, (l_x, l_y, rect_width, rect_height))
            box_node_array[i][j].set_position(l_x, l_y)
            box_node_array[i][j].set_positional_index(convert_pos_to_array_index((l_x, l_y)))
            l_x += 11
        l_x = 13
        l_y += 11

def mouse_event_handler(cur_pos, color = block_rect_color, other_node = False):
    for box_pos_x, box_pos_y in box_arrays:
        if (cur_pos[0] >= box_pos_x and cur_pos[0] <= (box_pos_x + rect_width)) and (cur_pos[1] >= box_pos_y and cur_pos[1] <= (box_pos_y + rect_height)):
            if not other_node:
                pygame.draw.rect(screen, color, (box_pos_x - 0.5, box_pos_y - 0.5, rect_width + 2, rect_height + 2))
            else:
                pygame.draw.rect(screen, color, (box_pos_x, box_pos_y, rect_width, rect_height))
            if blockers_btn_state:
                cur_index_value = convert_pos_to_array_index(cur_pos)
                box_node_array[cur_index_value[0]][cur_index_value[1]].node_type = 0

def dijkstras_algo_btn(color):
    global dijkstras_algo_btn_pos
    dijkstras_algo_btn_w = 100
    dijkstras_algo_btn_h = 30
    dijkstras_algo_btn_text = font_small.render("Dijkstra's", True, white)

    pygame.draw.rect(screen, color, (dijkstras_algo_btn_pos[0], clear_paths_btn_pos[1], dijkstras_algo_btn_w, dijkstras_algo_btn_h), width = 0, border_radius = 8)
    screen.blit(dijkstras_algo_btn_text, (dijkstras_algo_btn_pos[0] + dijkstras_algo_btn_w / 2 - dijkstras_algo_btn_text.get_width() / 2, dijkstras_algo_btn_pos[1] + dijkstras_algo_btn_h / 2 - dijkstras_algo_btn_text.get_height() / 2))

def clear_paths_btn():
    global clear_paths_btn_pos
    clear_paths_btn_w = 100
    clear_paths_btn_h = 30
    clear_paths_btn_text = font_small.render("Clear Path", True, pygame.Color(235, 20, 20))

    pygame.draw.rect(screen, clear_path_color, (clear_paths_btn_pos[0], clear_paths_btn_pos[1], clear_paths_btn_w, clear_paths_btn_h), width = 0, border_radius = 8)
    screen.blit(clear_paths_btn_text, (clear_paths_btn_pos[0] + clear_paths_btn_w / 2 - clear_paths_btn_text.get_width() / 2, clear_paths_btn_pos[1] + clear_paths_btn_h / 2 - clear_paths_btn_text.get_height() / 2))

def create_maze_btn():
    global maze_btn_pos
    maze_btn_w = 130
    maze_btn_h = 30
    maze_btn_text = font_small.render("Generate Maze", True, white)

    pygame.draw.rect(screen, generate_maze_btn_color, (maze_btn_pos[0], maze_btn_pos[1], maze_btn_w, maze_btn_h), width = 0, border_radius = 8)
    screen.blit(maze_btn_text, (maze_btn_pos[0] + maze_btn_w / 2 - maze_btn_text.get_width() / 2, maze_btn_pos[1] + maze_btn_h / 2 - maze_btn_text.get_height() / 2))


def reset_btn_logic():
    global reset_btn_pos
    reset_btn_w = 100
    reset_btn_h = 30
    reset_btn_text = font_small.render("Reset", True, white)

    pygame.draw.rect(screen, pygame.Color(235, 20, 20), (reset_btn_pos[0], reset_btn_pos[1], reset_btn_w, reset_btn_h), width = 0, border_radius = 8)
    screen.blit(reset_btn_text, (reset_btn_pos[0] + reset_btn_w / 2 - reset_btn_text.get_width() / 2, reset_btn_pos[1] + reset_btn_h / 2 - reset_btn_text.get_height() / 2))

def start_algo_btn(color):
    global start_algo_btn_pos
    start_algo_btn_w = 100
    start_algo_btn_h = 30
    start_algo_btn_text = font_small.render("A*", True, white)

    pygame.draw.rect(screen, color, (start_algo_btn_pos[0], start_algo_btn_pos[1], start_algo_btn_w, start_algo_btn_h), width = 0, border_radius = 8)    
    screen.blit(start_algo_btn_text, (start_algo_btn_pos[0] + start_algo_btn_w / 2 - start_algo_btn_text.get_width() / 2, start_algo_btn_pos[1] + start_algo_btn_h / 2 - start_algo_btn_text.get_height() / 2))

def blockers_box(color):
    global blockers_box_pos
    blockers_box_w = 130
    blockers_box_h = 30
    blockers_box_text = font_small.render("Draw Obstacle", True, black)

    pygame.draw.rect(screen, color, (blockers_box_pos[0], blockers_box_pos[1], blockers_box_w, blockers_box_h), width = 0, border_radius = 8)    
    screen.blit(blockers_box_text, (blockers_box_pos[0] + blockers_box_w / 2 - blockers_box_text.get_width() / 2, blockers_box_pos[1] + blockers_box_h / 2 - blockers_box_text.get_height() / 2))

def end_box_node(color):
    global end_box_node
    end_node_w = 90
    end_node_h = 30 
    end_node_text = font_small.render("End", True, white)

    pygame.draw.rect(screen, color, (end_box_pos[0], end_box_pos[1], end_node_w, end_node_h), width = 0, border_radius = 8)    
    screen.blit(end_node_text, (end_box_pos[0] + end_node_w / 2 - end_node_text.get_width() / 2, end_box_pos[1] + end_node_h / 2 - end_node_text.get_height() / 2))

def start_box_node(color):
    global start_box_pos
    start_node_w = 90
    start_node_h = 30  
    start_node_text = font_small.render("Start", True, white)

    pygame.draw.rect(screen, color, (start_box_pos[0], start_box_pos[1], start_node_w, start_node_h), width = 0, border_radius = 8)
    screen.blit(start_node_text, (start_box_pos[0] + start_node_w / 2 - start_node_text.get_width() / 2, start_box_pos[1] + start_node_h / 2 - start_node_text.get_height() / 2))

def contained(click_pos, box_pos, box_dim):
    return (click_pos[0] > box_pos[0] and click_pos[0] < box_pos[0] + box_dim[0] and click_pos[1] > box_pos[1] and click_pos[1] < box_pos[1] + box_dim[1])
        

def btn_classifier(click_pos):
    global start_btn_state
    global end_btn_state
    global blockers_btn_state
    global start_btn_clicked 
    global end_btn_clicked
    global path
    global node_list_complete
    global animation_started
    global maze_created
    global normal_flow
    global rows
    global cols
    global animation_index
    global animation_list 
    global path_index
    global dijkstras_btn_clickable
    global animation_completion 

    if contained(click_pos, start_box_pos, (120, 35)) and not start_btn_clicked:
        global start_btn_state
        start_btn_state = not start_btn_state
        start_btn_clicked = True
        if start_btn_state:
            start_box_node(start_green_col)
        else:
            start_box_node(start_green_dark_col)
        
    elif contained(click_pos, end_box_pos, (120, 35)) and not end_btn_clicked and start_btn_clicked:
        global end_btn_state

        end_btn_state = not end_btn_state
        end_btn_clicked = True
        if end_btn_state:
            end_box_node(orange_col)
        else:
            end_box_node(orange_dark_col)

    elif contained(click_pos, blockers_box_pos, (120, 35)) and start_btn_clicked and end_btn_clicked and not animation_started:
        global blockers_btn_clicked
        global blockers_btn_state
        global start_algo_btn_state

        blockers_btn_state = not blockers_btn_state
        if blockers_btn_state:
            blockers_box(white)
            blockers_btn_clicked = True
            start_algo_btn(start_algo_dark_col)
        else:
            blockers_box(off_white)
            if blockers_btn_clicked:
                start_algo_btn(start_algo_light_col)
                start_algo_btn_state = True
    
    elif contained(click_pos, start_algo_btn_pos, (160, 35)) and start_algo_btn_state and normal_flow:
        animation_started = True
        path = run_a_star_algorithm()
        node_list_complete = True
        normal_flow = False
        if maze_created:
            dijkstras_algo_btn(start_algo_dark_col)

    elif contained(click_pos, reset_btn_pos, (120, 30)):
        reset_all_vals()
        
    # 'Create Maze' Button
    elif contained(click_pos, maze_btn_pos, (120, 30)) and not maze_created and not start_btn_clicked:
        start_algo_btn_state = True
        animation_started = True
        create_maze()

    # 'Clearing the path' 
    elif contained(click_pos, clear_paths_btn_pos, (120, 30)) and animation_completion and maze_created:
        pygame.draw.rect(screen, box_background_color, (13, 131, 1341, 626))
        draw_rects()
        for i in range(rows):
            for j in range(cols):
                if maze[i][j] == 1:
                    pygame.draw.rect(screen, pygame.Color(50,50,50), (box_node_array[i][j].xdist_position - 0.5, box_node_array[i][j].ydist_position - 0.5, 11, 11))

        animation_started = True
        animation_index = 0
        animation_list = []
        path_index = 0
        path = []
        normal_flow = True
        dijkstras_btn_clickable = True
        dijkstras_algo_btn(start_algo_light_col)
        start_algo_btn(start_algo_light_col)
        animation_completion = False
        pygame.draw.rect(screen, start_green_col, (24 - 0.5, 131 - 0.5, 11, 11))
        pygame.draw.rect(screen, orange_col, (end_node_position[1] * 11 + 13 - 0.5, end_node_position[0] * 11 + 131 - 0.5, 11, 11))
        
    elif contained(click_pos, dijkstras_algo_btn_pos, (120, 30)) and dijkstras_btn_clickable and normal_flow:
        animation_started = True
        path = dijkstras_algorithm()
        node_list_complete = True
        start_algo_btn(start_algo_dark_col)
        normal_flow = False



def create_maze():
    global maze_created
    global maze
    global start_btn_clicked
    global end_btn_clicked 
    global start_node_position
    global end_node_position
    global rows
    global cols
    global draw_maze
    global normal_flow
    global dijkstras_btn_clickable

    # maze_created = True
    start_node_position = (0, 1)

    start_btn_clicked = True
    end_btn_clicked = True
    normal_flow = False
    dijkstras_btn_clickable = False
    maze = generate_maze()

    draw_maze = True
            
    if maze[56][120] == 1:
        end_node_position = (56, 119)
    else:
        end_node_position = (56, 120)


def reset_all_vals():
    global box_arrays 
    global animation_list
    global path
    global node_list_complete
    global path_list_complete
    global mouse_motion
    global start_btn_state 
    global end_btn_state
    global blockers_btn_state
    global start_algo_btn_state
    global start_btn_clicked
    global end_btn_clicked
    global blockers_btn_clicked
    global animation_completion
    global start_node_position
    global end_node_position
    global box_node_array
    global animation_index
    global path_index
    global path_time_gap 
    global no_path_found_state
    global maze_created
    global animation_started
    global maze
    global draw_maze
    global maze_index
    global maze_fill_time
    global normal_flow
    global dijkstras_btn_clickable 

    box_arrays = []
    animation_list = []
    path = []
    maze = []
    node_list_complete = False
    path_list_complete = False
    mouse_motion = False
    start_btn_state = False
    end_btn_state = False
    blockers_btn_state = False
    start_algo_btn_state = False
    start_btn_clicked = False
    end_btn_clicked = False
    blockers_btn_clicked = False
    animation_completion = False
    start_node_position = ()
    end_node_position = ()
    box_node_array = [[Node() for i in range(cols)] for j in range(rows)]
    animation_index = 0
    path_index = 0
    path_time_gap = 5
    no_path_found_state = False
    maze_created = False
    animation_started = False
    draw_maze = False
    maze_index = 0
    maze_fill_time = 5
    normal_flow = True
    dijkstras_btn_clickable = False

    draw_basic_UIs()


def draw_basic_UIs():
    screen.fill(background_color)
    pygame.draw.rect(screen, box_background_color, (13, 131, 1341, 626))
    draw_text()
    draw_rects()
    start_box_node(start_green_dark_col)
    end_box_node(orange_dark_col)
    blockers_box(off_white)
    start_algo_btn(start_algo_dark_col)
    reset_btn_logic()
    create_maze_btn()

def draw_green_node(clicked_pos):
    global start_btn_state
    global start_node_position

    mouse_event_handler(clicked_pos, start_green_col, True)
    start_btn_state = False
    start_box_node(start_green_dark_col)
    start_node_position = convert_pos_to_array_index(clicked_pos)
    box_node_array[start_node_position[0]][start_node_position[1]].node_type = 1

def draw_orange_node(clicked_pos):
    global end_btn_state
    global end_node_position

    mouse_event_handler(clicked_pos, orange_col, True)
    end_btn_state = False
    end_box_node(orange_dark_col)
    end_node_position = convert_pos_to_array_index(clicked_pos)
    box_node_array[start_node_position[0]][start_node_position[1]].node_type = -1

def convert_pos_to_array_index(pos):
    x_val = 0
    y_val = 0
    x, y = pos
    x -= 13
    y -= 131
    while x >= 0:
        x -= 11
        x_val += 1
    while y >= 0:
        y -= 11
        y_val += 1

    return (y_val - 1, x_val - 1) 

def calculate_val(pos):
    global cols
    return pos[0] + pos[1] * cols 

def run_a_star_algorithm(allow_diagonal_movement = False):
    global maze
    global start_node_position
    global end_node_position

    start_index = start_node_position
    end_index = end_node_position

    global cols 
    global rows
    global animation_list

    if not maze_created:
        maze = [[0 for i in range(cols)] for j in range(rows)]

        for i in range(rows):
            for j in range(cols):
                if box_node_array[i][j].node_type == 0:
                    maze[i][j] = 1

    start_node = Node(None, start_index)
    start_node.g = start_node.h = start_node.f = 0

    end_node = Node(None, end_index)
    end_node.g = end_node.h = end_node.f = 0

    for i in range(rows):
        for j in range(cols):
            box_node_array[i][j].in_close_list = False
            box_node_array[i][j].in_open_list = False

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)
    box_node_array[start_node.position[0]][start_node.position[1]].in_open_list = True

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = 50000

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    current_node = Node()
    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
          # if we hit this point return the path such as it is
          # it will not contain the destination
          warn("giving up on pathfinding too many iterations")
          return return_path(current_node)       
        
        # Get the current node
        current_node = heapq.heappop(open_list)
            
        closed_list.append(current_node)
        box_node_array[current_node.position[0]][current_node.position[1]].in_open_list = False
        box_node_array[current_node.position[0]][current_node.position[1]].in_close_list = True
        
        animation_list.append({"pos": current_node.position, "color": pygame.Color(255,0,0)})
        animation_list.append({"pos": current_node.position, "color": current_node_fill_color})

        # Found the goal
        if current_node == end_node:
            print("Animation objects number: ", len(animation_list))
            print("Iteration number: ", outer_iterations)
            return return_path(current_node)

        # Generate children
        children = []
        
        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if box_node_array[child.position[0]][child.position[1]].in_close_list:
                continue

            # Create the f, g, and h values

            # Euclidean Heuristic Distance Value
            child.g = current_node.g + 1
            child.h = abs((child.position[0] - end_node.position[0])) + abs((child.position[1] - end_node.position[1]))

            # Manhattan Heuristic Distance Value
            # child.h = 2 * (abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1]))

            child.f = child.g + child.h
                
            if box_node_array[child.position[0]][child.position[1]].in_open_list:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)
            box_node_array[child.position[0]][child.position[1]].in_open_list = True
            animation_list.append({"pos": child.position, "color": open_list_node_fill_color})
           
    warn("Couldn't get a path to destination")
    no_path_found()
    return None

def dijkstras_algorithm():
    global maze
    global start_node_position
    global end_node_position

    start_index = start_node_position
    end_index = end_node_position

    global cols 
    global rows
    global animation_list

    if not maze_created:
        maze = [[0 for i in range(cols)] for j in range(rows)]

        for i in range(rows):
            for j in range(cols):
                if box_node_array[i][j].node_type == 0:
                    maze[i][j] = 1

    start_node = Node(None, start_index)
    start_node.g = start_node.h = start_node.f = 0

    end_node = Node(None, end_index)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize the node's cost values to large number
    for i in range(rows):
        for j in range(cols):
            box_node_array[i][j].in_close_list = False
            box_node_array[i][j].in_open_list = False
            if maze[i][j] == 1:
                    box_node_array[i][j].f = 1000

    box_node_array[start_index[0]][start_index[1]].f = 0

    open_list = []
    closed_list = []

    starting_node = box_node_array[start_index[0]][start_index[1]]

    heapq.heapify(open_list)
    heapq.heappush(open_list, starting_node)

    box_node_array[start_node.position[0]][start_node.position[1]].in_open_list = True

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = 50000

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0))

    current_node = Node()
    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
          # if we hit this point return the path such as it is
          # it will not contain the destination
          warn("giving up on pathfinding too many iterations")
          return return_path(current_node)       
        
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)
        box_node_array[current_node.position[0]][current_node.position[1]].in_open_list = False
        box_node_array[current_node.position[0]][current_node.position[1]].in_close_list = True

        animation_list.append({"pos": current_node.position, "color": pygame.Color(255,0,0)})
        animation_list.append({"pos": current_node.position, "color": current_node_fill_color})

        # Found the goal
        if current_node == end_node:
            print("Animation objects number: ", len(animation_list))
            print("Iteration number: ", outer_iterations)
            return return_path(current_node)

        # Generate children
        children = []
        
        for new_position in adjacent_squares: # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            # Create new node
            new_node = Node(current_node, node_position)
            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            if box_node_array[child.position[0]][child.position[1]].in_close_list:
                continue

            temp_distance = current_node.f + 1

            if temp_distance < child.f:
                child.f = temp_distance
                child.parent = current_node

            box_node_array[child.position[0]][child.position[1]].f = child.f
            box_node_array[child.position[0]][child.position[1]].parent = current_node

            if box_node_array[child.position[0]][child.position[1]].in_open_list:
                for node in open_list:
                    if node == child:
                        node.f = temp_distance
                        node.parent = current_node
            else:
                heapq.heappush(open_list, box_node_array[child.position[0]][child.position[1]])
                box_node_array[child.position[0]][child.position[1]].in_open_list = True
            animation_list.append({"pos": child.position, "color": open_list_node_fill_color})
           
    warn("Couldn't get a path to destination")
    no_path_found()
    return None

def no_path_found():
    global no_path_found_state 
    no_path_found_state = True
    no_path_text = font_medium.render("No Path Found", True, current_node_fill_color)
    screen.blit(no_path_text, (980, 80))

draw_basic_UIs()

animation_index = 0
path_index = 0
time_gap = -1
path_time_gap = 5
maze_index = 0
maze_fill_time = 5

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if blockers_btn_state:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_motion = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_motion = False
        
        if start_btn_state:
            if event.type == pygame.MOUSEBUTTONDOWN:
                draw_green_node(pygame.mouse.get_pos())

        if end_btn_state:
            if event.type == pygame.MOUSEBUTTONDOWN:
                draw_orange_node(pygame.mouse.get_pos())
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            btn_classifier(pygame.mouse.get_pos())
    
    if draw_maze:
        if maze_fill_time < 0:
            maze_fill_time = 5

            for i in range(cols):
                ith_value = maze_index
                jth_value = i
                if maze[ith_value][jth_value] == 1:
                    pygame.draw.rect(screen, pygame.Color(50,50,50), (box_node_array[ith_value][jth_value].xdist_position - 0.5, box_node_array[ith_value][jth_value].ydist_position - 0.5, 11, 11))
            maze_index += 1
            if maze_index == rows:
                draw_maze = False
                maze_created = True
                normal_flow = True
                dijkstras_btn_clickable = True
                pygame.draw.rect(screen, start_green_col, (24 - 0.5, 131 - 0.5, 11, 11))
                pygame.draw.rect(screen, orange_col, (end_node_position[1] * 11 + 13 - 0.5, end_node_position[0] * 11 + 131 - 0.5, 11, 11))
                start_algo_btn(start_algo_light_col)
                dijkstras_algo_btn(start_algo_light_col)
        else:
            maze_fill_time -= 1

    if node_list_complete:
        x_pos, y_pos = animation_list[animation_index]["pos"]

        pygame.draw.rect(screen, animation_list[animation_index]["color"], (animation_list[animation_index]["pos"][1] * 11 + 13, animation_list[animation_index]["pos"][0] * 11 + 131, 10, 10))
        if animation_index + 1 == len(animation_list):
            node_list_complete = False
            path_list_complete = True
            pygame.draw.rect(screen, start_green_dark_col, (start_node_position[1] * 11 + 13 - 0.5, start_node_position[0] * 11 + 131 - 0.5, rect_width + 2, rect_height + 2))
        else:
            animation_index += 1

    if path_list_complete and not no_path_found_state:
        if path_time_gap < 0:
            path_time_gap = 5
            if path_index + 1 != len(path):
                pygame.draw.line(screen, pygame.Color(235, 40, 40), (path[path_index][1] * 11 + 13 + 4, path[path_index][0] * 11 + 131 + 4), (path[path_index + 1][1] * 11 + 13 + 4, path[path_index + 1][0] * 11 + 131 + 4), 3)

            if path_index + 1 == len(path):
                path_list_complete = False
                animation_completion = True
                pygame.draw.rect(screen, pygame.Color(235,40,40), (end_node_position[1] * 11 + 13 - 0.5, end_node_position[0] * 11 + 131 - 0.5, rect_width + 2, rect_height + 2))
                print("Path Calculated: ", len(path), " units")
                if maze_created:
                    dijkstras_algo_btn(start_algo_dark_col)
                    start_algo_btn(start_algo_dark_col)
                    clear_paths_btn()
                
            else:
                path_index += 1
        else:
            path_time_gap -= 1
    
    if mouse_motion and blockers_btn_state:
        mouse_event_handler(pygame.mouse.get_pos())
            
    pygame.display.update()
    fps_clock.tick(fps)