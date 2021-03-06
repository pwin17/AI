import argparse
from collections import deque
import time

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

def bfs(maze, position):
    """2D maze, x and y coordinates of the starting point as input and returns goal status"""
    frontier = []
    if position[0]-1 >= 0 and maze.m[position[0]-1][position[1]].status != "%" and maze.m[position[0]-1][position[1]].traveled == False: #checks if north is a valid node
        if maze.m[position[0]-1][position[1]].status ==".": #checks if north reaches a goal
            maze.m[position[0]-1][position[1]].parent = maze.m[position[0]][position[1]]
            return ["found",position[0]-1,position[1]]
        maze.m[position[0]-1][position[1]].traveled = True #marks north as traveled
        maze.m[position[0]-1][position[1]].parent = maze.m[position[0]][position[1]] #marks parent of north as current
        frontier.append([position[0]-1,position[1]]) #appends north to frontier

    if position[1]+1 <= maze.row_length-1 and maze.m[position[0]][position[1]+1].status != "%" and maze.m[position[0]][position[1]+1].traveled == False:
        if maze.m[position[0]][position[1]+1].status ==".":
            maze.m[position[0]][position[1]+1].parent = maze.m[position[0]][position[1]]
            return ["found",position[0],position[1]+1]
        maze.m[position[0]][position[1]+1].traveled = True
        maze.m[position[0]][position[1]+1].parent = maze.m[position[0]][position[1]]
        frontier.append([position[0],position[1]+1])
    if position[0]+1 <= maze.column_length-1 and maze.m[position[0]+1][position[1]].status != "%" and maze.m[position[0]+1][position[1]].traveled == False:
        if maze.m[position[0]+1][position[1]].status ==".":
            maze.m[position[0]+1][position[1]].parent = maze.m[position[0]][position[1]]
            return ["found",position[0]+1,position[1]]
        maze.m[position[0]+1][position[1]].traveled = True
        maze.m[position[0]+1][position[1]].parent = maze.m[position[0]][position[1]]
        frontier.append([position[0]+1,position[1]])
    if position[1]-1 >= 0 and maze.m[position[0]][position[1]-1].status != "%" and maze.m[position[0]][position[1]-1].traveled == False:
        if maze.m[position[0]][position[1]-1].status ==".":
            maze.m[position[0]][position[1]-1].parent = maze.m[position[0]][position[1]]
            return ["found",position[0],position[1]-1]
        maze.m[position[0]][position[1]-1].traveled = True
        maze.m[position[0]][position[1]-1].parent = maze.m[position[0]][position[1]]
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
            if f != "\n":
                maze.m[y][x] = Node(f) #Walls and paths
                x+=1
        y+=1
    
    #BFS using FIFO 
    our_deque = deque()
    our_deque.append([sp[0],sp[1]])
    maze.m[sp[0]][sp[1]].traveled = True
    expanded_nodes = 0
    path_cost = 0
    while our_deque != []:
        transition = bfs(maze, our_deque[0])
        #Goal Test
        if transition:
            if transition[0] == "found": #found prize
                current = maze.m[transition[1]][transition[2]]
                x = 100
                while current.parent != None:
                    if current.parent.status != "P":
                        current.parent.status = "#"
                    path_cost+=1
                    current = current.parent
                break
            else:
                for i in transition:
                    our_deque.append(i)
                    expanded_nodes+=1
        else:
            our_deque.popleft()

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takes in maze file location and outputs")
    parser.add_argument('-i', '--input_file', type=str, metavar='', help='Name of file location')
    try:
        args = parser.parse_args()
        single_bfs(args.input_file)
    except:
        time1 = time.time()
        single_bfs("./lab_a_files/1prize-open.txt")
        print(f"Runtime for 1prize-open.txt: {round(time.time() - time1,5)}\n")
        time2 = time.time()
        single_bfs("./lab_a_files/1prize-medium.txt")
        print(f"Runtime for 1prize-medium.txt: {round(time.time() - time2,5)}\n")
        time3 = time.time()
        single_bfs("./lab_a_files/1prize-large.txt")
        print(f"Runtime for 1prize-large.txt: {round(time.time() - time3,5)}\n")