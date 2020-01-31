import argparse
from collections import deque
#hash table to store traveled
#traveled_set[00] = True
#example: If examining north:
#           if (x,y) not in traveled_set:
#              add to frontier
#When checking in the array, we need to account for negative x,y values and x,y values greater than row_length and column_length
class Node():
    def __init__(self, status="0", parent=None, ):
        self.status = status
        self.parent = parent
        self.traveled = False
class Maze():
    def __init__(self,maze,row_length,column_length):
        self.m = maze
        self.row_length = row_length
        self.column_length = column_length

#Transition Function that takes in a maze and a starting point and performs a NESW search
def dfs(position, maze):
    if position[0]-1 >= 0 and maze.m[position[0]-1][position[1]].status != "%" and maze.m[position[0]-1][position[1]].traveled == False:
        if maze.m[position[0]-1][position[1]].status ==".":
            return "found"
        maze.m[position[0]-1][position[1]].traveled = True
        maze.m[position[0]-1][position[1]].parent = maze.m[position[0]][position[1]]
        maze.m[position[0]-1][position[1]].status = "#"
        return [position[0]-1,position[1]]
    elif position[1]+1 <= maze.row_length-1 and maze.m[position[0]][position[1]+1].status != "%" and maze.m[position[0]][position[1]+1].traveled == False:
        if maze.m[position[0]][position[1]+1].status ==".":
            return "found"
        maze.m[position[0]][position[1]+1].traveled = True
        maze.m[position[0]][position[1]+1].parent = maze.m[position[0]][position[1]]
        maze.m[position[0]][position[1]+1].status = "#"
        return [position[0],position[1]+1]
    elif position[0]+1 <= maze.column_length-1 and maze.m[position[0]+1][position[1]].status != "%" and maze.m[position[0]+1][position[1]].traveled == False:
        if maze.m[position[0]+1][position[1]].status ==".":
            return "found"
        maze.m[position[0]+1][position[1]].traveled = True
        maze.m[position[0]+1][position[1]].parent = maze.m[position[0]][position[1]]
        maze.m[position[0]+1][position[1]].status = "#"
        return [position[0]+1,position[1]]
    elif position[1]-1 >= 0 and maze.m[position[0]][position[1]-1].status != "%" and maze.m[position[0]][position[1]-1].traveled == False:
        if maze.m[position[0]][position[1]-1].status ==".":
            return "found"
        maze.m[position[0]][position[1]-1].traveled = True
        maze.m[position[0]][position[1]-1].parent = maze.m[position[0]][position[1]]
        maze.m[position[0]][position[1]-1].status = "#"
        return [position[0],position[1]-1]
    else:
        return False
def single_dfs(file_location):
    file = open(f"{file_location}", "r")    
    row_length = len(file.readline())-1 #more concise than for loop
    column_length = len(file.readlines())+1 #more concise than for loop
    file.seek(0)
    maze = Maze([[0 for x in range(row_length)] for y in range(column_length)], row_length, column_length)
    y = 0
    prizes = []
    for i in file.readlines():
        x = -1
        for f in i:
            if f == "P":
                sp = [y,x+1]
            if f == ".":
                prizes.append([y,x])
            if f != "\n":
                x+=1
                maze.m[y][x] = Node(f)
        y+=1

    #DFS uses a stack LIFO
    our_stack = [[sp[0],sp[1]]]
    maze.m[sp[0]][sp[1]].traveled = True
    #To print the maze
    # for i in maze.m:
    #     x = []
    #     for f in i:
    #         x.append(f.status)
    #     print(x)
    expanded_nodes = 0
    path_cost = 0
    while our_stack != []:
        transition = dfs(our_stack[len(our_stack)-1], maze)
        #Goal Test
        if transition:
            expanded_nodes+=1
            path_cost+=1
            if transition == "found": #found prize
                break
            our_stack.append(transition)
        else:
            path_cost-=1
            unmark = our_stack.pop()
            maze.m[unmark[0]][unmark[1]].status = " "
    for i in maze.m:
        x = ""
        for f in i:
            x+=f.status
        print(x)
    print(f"Path Cost: {path_cost}\nExpanded Nodes: {expanded_nodes}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takes in maze file location and outputs")
    parser.add_argument('-i', '--input_file', type=str, metavar='', help='Name of file location')

    args = parser.parse_args()
    single_dfs(args.input_file)