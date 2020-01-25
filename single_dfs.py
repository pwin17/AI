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

def single_dfs(file_location):
    file = open(f"{file_location}", "r")
    maze = []
    position = 0
    row_length = 0
    column_length = 0
    for i in file.readline():
        row_length+=1
    for i in file.readlines():
        column_length+=1
    file.seek(0)
    maze = [[Node()]*row_length]*column_length
    # column = 0
    # for i in file.readlines():
    #     row = 0
    #     for f in i:
    #         print(row)
    #         maze[column][row].status = f
    #         row+=1
    #     column+=1
    # for i in maze:
    #     for f in i:
    #         print(f.status)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takes in maze file location and outputs")
    parser.add_argument('-i', '--input_file', type=str, metavar='', help='Name of file location')

    args = parser.parse_args()
    single_dfs(args.input_file)