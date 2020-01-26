import argparse
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

#New function that takes in a maze and a starting point and performs DFS 
#def dfs(node, maze):
def single_dfs(file_location):
    file = open(f"{file_location}", "r")
    row_length = len(file.readline())-1
    column_length = len(file.readlines())+1
    file.seek(0)
    maze = [[0 for x in range(row_length)] for y in range(column_length)]
    y = 0
    for i in file.readlines():
        x = -1
        for f in i:
            if f == "P":
                sp = [y,x]
            if f != "\n":
                x+=1
                maze[y][x] = Node(f)
        y+=1
    our_stack = [maze[sp[0]][sp[1]]]
    while our_stack != []:
        break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takes in maze file location and outputs")
    parser.add_argument('-i', '--input_file', type=str, metavar='', help='Name of file location')

    args = parser.parse_args()
    single_dfs(args.input_file)