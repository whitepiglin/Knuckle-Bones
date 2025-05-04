def calculate_score(board):
    score = 0
    columns = [[] for i in range(0,len(board[0]))]
    for row in board:
        for i in range(0,len(row)):
            columns[i].append(row[i])
    for column in columns:
        while len(column):
            num = column[0]
            count = column.count(num)
            if count > 1:
                score += (num + num) * count
                for i in range(0,count):
                    column.remove(num)
            else:
                score += num
                column.remove(num)
    return score
        

def remove_dice(board,column,number):
    for row in board:
        if row[column] == number:
            row[column] = 0
    return board

def flip_board(board):
    board.reverse()
    for row in board:
        row.reverse()
    return board

def calculate_rect(grid,pos):
    box_size = [168*3/grid,159*3/grid]
    box_space = [(827-box_size[0]*grid)/(grid-1),(498-box_size[1]*grid)/(grid-1)]
    box_rect = [[0 for j in range(0,grid)] for i in range(0,grid)]
    for i in range(0,grid):
        for j in range(0,grid):
            rect = (pos[0]+(box_space[0]+box_size[0])*j,pos[1]+(box_space[1]+box_size[1])*i,box_size[0],box_size[1])
            box_rect[i][j] = rect
    return box_rect

def finish_board(board):
    count = 0
    for row in board:
        count += row.count(0)
    if count:
        return False
    else:
        return True
    
def resolve_matches_string(string:str):
    result = []
    string = string.replace("[","").replace("]","").replace("{","").split("}")[:-1]
    for i in range(0,len(string)):
        stringdict = {}
        string[i] = string[i].replace("'","").split(", ")
        if i > 0:
            string[i] = string[i][1:]
        for s in string[i]:
            s = s.replace("'","").split(": ")
            stringdict[s[0]] = s[1] if s[0] != "Size" and s[0] != "Player" else int(s[1])
        result.append(stringdict)
    return result

def resolve_match_string(string:str):
    if string == "None" or string == "Ended":
        return string
    result = {}
    string = string.replace("{","").replace("}","").replace("'","")
    boards = []
    temp = ""
    front = 0
    back = 0
    start = False
    for s in string:
        if s == "[":
            start = True
            front += 1
            temp += s
        elif s == "]":
            back += 1
            temp += s
            if front == back:
                boards.append(temp)
                temp = ""
                start = False
        else:
            if start:
                temp += s
    string = string.split(", ")
    start = True
    for s in string:
        s = s.replace("'","").split(": ")
        if s[0] == "Player 1 Score" or s[0] == "Rematch":
            start = True
        if start:
            result[s[0]] = int(s[1]) if s[0] != "Match Code" and s[0] != "Match Name" else s[1]
        if s[0] == "Grid" or s[0] == "Dice":
            start = False
    result["Placed"] = boards[result["Size"]]
    for i in range(0,result["Size"]):
        result[f"Player {i+1} Board"] = boards[i]
    return result

def resolve_board_string(string:str):
    result = []
    string = string.replace("[","").split("]")[:-2]
    for i in range(0,len(string)):
        stringlist = []
        string[i] = string[i].replace("'","").split(", ")
        if i > 0:
            string[i] = string[i][1:]
        for s in string[i]:
            stringlist.append(int(s))
        result.append(stringlist)
    return result

def resolve_placed_string(string:str):
    result = []
    string = string.replace("[","").replace("]","").split(", ")
    size = len(string)//2
    for i in range(0,size+1,2):
        result.append([int(string[i]),int(string[i+1])])
    return result
