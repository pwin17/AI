
import argparse
from collections import deque
import math
from scipy.spatial import distance

class Node():
    def __init__(self, status = "0", parent = None):
        self.status = status
        self.parent = parent
        self.heuristic = 0
        # self.east = None
        # self.west = None
        # self.south = None
        self.traveled = False
    
class Maze():
    def __init__(self, maze, row_length, column_length):
        self.m = maze
        self.row_length = row_length
        self.column_length = column_length

class Heuristic():
    def __init__(self, position, heuristic):
        self.position = position
        self.heuristic = heuristic

def bfs(maze, position):
    """2D maze, x and y coordinates of the starting point as input and returns goal status"""
    frontier = []
    debug = True
    #calculate manhattan distance of NESW, then go based on best choice
    if position[0]-1 >= 0 and maze.m[position[0]-1][position[1]].status != "%" and maze.m[position[0]-1][position[1]].traveled == False: #checks if north is a valid node
        if maze.m[position[0]-1][position[1]].status ==".": #checks if north reaches a goal
            maze.m[position[0]-1][position[1]].parent = maze.m[position[0]][position[1]]
            return ["found",position[0]-1,position[1]]
        maze.m[position[0]-1][position[1]].parent = maze.m[position[0]][position[1]] #marks parent of north as current
        maze.m[position[0]-1][position[1]].traveled = True #marks north as traveled
        if debug:
            maze.m[position[0]-1][position[1]].status = "E"
        frontier.append([position[0]-1,position[1]]) #appends north to frontier

    if position[1]+1 <= maze.row_length-1 and maze.m[position[0]][position[1]+1].status != "%" and maze.m[position[0]][position[1]+1].traveled == False:
        if maze.m[position[0]][position[1]+1].status ==".":
            maze.m[position[0]][position[1]+1].parent = maze.m[position[0]][position[1]]
            return ["found",position[0],position[1]+1]
        maze.m[position[0]][position[1]+1].parent = maze.m[position[0]][position[1]]
        maze.m[position[0]][position[1]+1].traveled = True #marks north as traveled
        if debug:
            maze.m[position[0]][position[1]+1].status = "E"
        frontier.append([position[0],position[1]+1])
    if position[0]+1 <= maze.column_length-1 and maze.m[position[0]+1][position[1]].status != "%" and maze.m[position[0]+1][position[1]].traveled == False:
        if maze.m[position[0]+1][position[1]].status ==".":
            maze.m[position[0]+1][position[1]].parent = maze.m[position[0]][position[1]]
            return ["found",position[0]+1,position[1]]
        maze.m[position[0]+1][position[1]].parent = maze.m[position[0]][position[1]]
        maze.m[position[0]+1][position[1]].traveled = True #marks north as traveled
        if debug:
            maze.m[position[0]+1][position[1]].status = "E"
        frontier.append([position[0]+1,position[1]])
    if position[1]-1 >= 0 and maze.m[position[0]][position[1]-1].status != "%" and maze.m[position[0]][position[1]-1].traveled == False:
        if maze.m[position[0]][position[1]-1].status ==".":
            maze.m[position[0]][position[1]-1].parent = maze.m[position[0]][position[1]]
            return ["found",position[0],position[1]-1]
        maze.m[position[0]][position[1]-1].parent = maze.m[position[0]][position[1]]
        maze.m[position[0]][position[1]-1].traveled = True #marks north as traveled
        if debug:
            maze.m[position[0]][position[1]-1].status = "E"
        frontier.append([position[0],position[1]-1])
    return frontier
    
    # if 0 <= x_pos <= maze.column_length-2 and 0 <= y_pos <= maze.row_length:
    #     if maze.m[x_pos][y_pos].status == ".":
    #         return "found"

def single_bfs(file_path):
    infile = open(file_path, "r")
    row_length = len(infile.readline())-1 #excluding '\n'
    col_length = len(infile.readlines())+1 #first line plus the rest
    infile.seek(0)
    #Create 2D array
    maze = Maze([[0 for x in range(row_length)] for y in range(col_length)], row_length, col_length)
    y = 0
    prizes = []
    #create maze
    for i in infile.readlines():
        x = 0
        for f in i:
            if f == "P":
                sp = [y,x] #starting point
            if f == ".":
                prizes.append([y,x]) #prize location
                ep = [y,x]
            if f != "\n":
                maze.m[y][x] = Node(f) #Walls and paths
                x+=1
        y+=1
    


    #GBFS using FIFO 
    our_deque = []
    initial_heuristic = abs(ep[0] - sp[0]) + abs(ep[1] - sp[1]) + distance.euclidian(ep,sp)
    our_deque.append([initial_heuristic,[sp[0],sp[1]]])
    maze.m[sp[0]][sp[1]].traveled = True
    expanded_nodes = 0
    path_cost = 0
    debug = True
    debug_count = 0
    while our_deque != []:
        transition = bfs(maze, our_deque[0][1])
        #Goal Test

        if debug:
            if debug_count % 50 == 0:
                for i in maze.m:
                    x = ""
                    for f in i:
                        x+=f.status
                    print(x)
        debug_count+=1
        if transition:
            if transition[0] == "found": #found prize
                current = maze.m[transition[1]][transition[2]]
                while current.parent != None:
                    if current.parent != "P":
                        current.parent.status = "O"
                    path_cost+=1
                    current = current.parent
                break
            else:
                md_list =[]
                for i in transition:
                    maze.m[i[0]][i[1]].parent.heuristic +=1
                    md_list.append(abs(ep[0] - i[0]) + abs(ep[1] - i[1])+distance.euclidian(ep,i) + maze.m[i[0]][i[1]].parent.heuristic)
                for i in range(len(md_list)):
                    transition[i] = [md_list[i],transition[i]]
                for i in transition:
                    our_deque.append(i)
                    expanded_nodes+=1

                    # #[position1N, position2E, position3S]
                    # #calculate heuristics
                    # #
                    # #[heuristic1, heuristic2, heuristic3] take minimum
                    # #position = 0
                    # #min = something
                    # #for i in range(len(heuristic_list)):
                    # #
                    
                    # our_deque.append(i)
                    # expanded_nodes+=1
        else:
            our_deque.pop(0)
        our_deque = sorted(our_deque, key = lambda y: y[0])


    for i in maze.m:
        x = ""
        for f in i:
            x+=f.status
        print(x)
    print(f"Path Cost: {path_cost}\nExpanded Nodes: {expanded_nodes}")
    

    '''for i in maze.m:
        x = ""
        for f in i:
            x+=f.status
        print(x)'''

    
# parser = argparse.ArgumentParser(description="Takes in maze file location and outputs")
# parser.add_argument('-i', '--input_file', type=str, metavar='', help='Name of file location')
# args = parser.parse_args()

single_bfs("./lab_a_files/1prize-large.txt")