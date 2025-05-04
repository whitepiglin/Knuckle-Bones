import socket
import os
import shutil
import random
import json

from mechanic import *

host = socket.gethostbyname(socket.gethostname())
port = 8088
GAME = './Games/'

def create_game(grid,match_name,match_code,match_type):
    if match_code == "":
        match_code = generate_code()
    match_type = "Public/" if match_type == "True" else "Private/"
    data = {
        "Match Code": match_code,
        "Match Name": match_name,
        "Size": 2,
        "Player": 0,
        "Grid": grid,
        "Player 1 Board": [[0 for j in range(0,grid)] for i in range(0,grid)],
        "Player 2 Board": [[0 for j in range(0,grid)] for i in range(0,grid)],
        "Player 1 Score": 0,
        "Player 2 Score": 0,
        "Turn": random.randint(0,1),
        "Round": 0,
        "Dice": random.randint(1,6),
        "Placed": [[-1,-1] for i in range(0,2)]
    }
    with open(f"{GAME}{match_type}{match_code}.json","w") as file:
        file.write(json.dumps(data,indent=1,ensure_ascii=False))
    return match_code

def match_code_exist(match_code):
    exist = os.path.exists(f"{GAME}Public/{match_code}.json")
    if exist:
        return "Public/"
    exist = os.path.exists(f"{GAME}Private/{match_code}.json")
    if exist:
        return "Private/"
    exist = os.path.exists(f"{GAME}Ended/{match_code}.json")
    if exist:
        return "Ended/"
    else:
        return False

def match_ended(match_code):
    exist = os.path.exists(f"{GAME}Ended/{match_code}.json")
    return exist

def generate_code():
    exist_id = []
    id = ""
    for i in range(0,5):
        x = random.randint(0,9)
        id.append(x)
    for file in os.listdir(GAME):
        exist_id.append(file.split(".")[0])
    while id in exist_id:
        for i in range(0,5):
            x = random.randint(0,9)
            id.append(x)
    return id
    
def shuffle_list(list):
    result = []
    while len(list):
        obj = list[random.randint(0,len(list)-1)]
        result.append(obj)
        list.remove(obj)
    return result

class Server():
    def __init__(self,host,port,total_client, encode_format = 'utf-8', decode_format = 'utf-8', receive_size = 1024):
        self.host = host
        self.port = port
        self.total_client = total_client
        self.encode_format = encode_format
        self.decode_format = decode_format
        self.receive_size = receive_size
        
    def run(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
        print(f"Host: {self.host}, Port: {self.port}")
        server.bind((self.host,self.port))
        server.listen(self.total_client)
        activate = True
        while activate:
            conn, addr = server.accept()
            print('Connected by ', addr)
            command = conn.recv(self.receive_size).decode(self.decode_format)
            print(f"[CLIENT] {command}")
            content = command.split(":")[1]
            command = command.split(":")[0]
            if command == "create_game":
                grid = int(content.split(',')[0])
                match_name = content.split(',')[1]
                match_code = content.split(',')[2]
                match_type = content.split(',')[3]
                if match_code_exist(match_code):
                    conn.send(f"Error Code 1550: Match already exist".encode(self.encode_format))
                else:
                    id = create_game(grid,match_name,match_code,match_type)
                    conn.send(f"{id}".encode(self.encode_format))
            elif command == "get_match":
                match_id = content
                match_type = match_code_exist(match_id)
                if not match_type:
                    conn.send(f"Error Code 1402: Match not exist".encode(self.encode_format))
                else:
                    if match_ended(match_id):
                        conn.send(f"Error Code 202: Match ended".encode(self.encode_format))
                    else:
                        with open(f"{GAME}{match_type}{match_id}.json","r") as file:
                            data = json.load(file)
                        conn.send(f"{data}".encode(self.encode_format))
            elif command == "get_ended_match":
                match_id = content
                if match_ended(match_id):
                    with open(f"{GAME}Ended/{match_id}.json","r") as file:
                        data = json.load(file)
                    conn.send(f"{data}".encode(self.encode_format))
                else:
                    conn.send(f"Error Code 201: Match deleted".encode(self.encode_format))
            elif command == "update_match":
                match_id = content.split(',')[0]
                section = content.split(',')[1]
                action = content.split(',')[2]
                match_type = match_code_exist(match_id)
                if section == "Type":
                    shutil.move(f"{GAME}{match_type}{match_id}.json",f"{GAME}{action}/{match_id}.json")
                elif "Board" in section:
                    temp = content.split(',')[2:]
                    action = ""
                    for t in temp:
                        action += t
                    action = action.replace("(","").replace(")","").split(" ")
                    for i in range(0,len(action)):
                        action[i] = int(action[i])
                    with open(f"{GAME}{match_type}{match_id}.json","r") as file:
                        data = json.load(file)
                    if section == "Player 1 Board":
                        data["Player 1 Board"][action[0]][action[1]] = data["Dice"]
                        action[1] = (action[1] - (data["Grid"]-1)) * -1
                        remove_dice(data["Player 2 Board"],action[1],data["Dice"])
                        data["Placed"][data["Turn"]] = [action[0],action[1]]
                        data["Turn"] = 1
                    else:
                        data["Player 2 Board"][action[0]][action[1]] = data["Dice"]
                        action[1] = (action[1] - (data["Grid"]-1)) * -1
                        remove_dice(data["Player 1 Board"],action[1],data["Dice"])
                        data["Placed"][data["Turn"]] = [action[0],action[1]]
                        data["Turn"] = 0
                    data["Dice"] = random.randint(1,6)
                    data["Player 1 Score"] = calculate_score(data["Player 1 Board"])
                    data["Player 2 Score"] = calculate_score(data["Player 2 Board"])
                    with open(f"{GAME}{match_type}{match_id}.json","w") as file:
                        file.write(json.dumps(data,indent=1,ensure_ascii=False))
                    if finish_board(data["Player 1 Board"]) or finish_board(data["Player 2 Board"]):
                        shutil.move(f"{GAME}{match_type}{match_id}.json",f"{GAME}Ended/{match_id}.json")
                        with open(f"{GAME}Ended/{match_id}.json","r") as file:
                            data = json.load(file)
                        data["Rematch"] = 0
                        with open(f"{GAME}Ended/{match_id}.json","w") as file:
                            file.write(json.dumps(data,indent=1,ensure_ascii=False))
                elif section == "Placed":
                    temp = content.split(',')[1:]
                    action = ""
                    for t in temp:
                        action += t
                    action = action.replace("[","").replace("]","").split(", ")
                    with open(f"{GAME}{match_type}{match_id}.json","r") as file:
                        data = json.load(file)
                    data[section][int(action[0])] = [int(action[1]),int(action[1])]
                    with open(f"{GAME}{match_type}{match_id}.json","w") as file:
                        file.write(json.dumps(data,indent=1,ensure_ascii=False))
                else:
                    with open(f"{GAME}{match_type}{match_id}.json","r") as file:
                        data = json.load(file)
                    data[section] = int(action)
                    with open(f"{GAME}{match_type}{match_id}.json","w") as file:
                        file.write(json.dumps(data,indent=1,ensure_ascii=False))
            elif command == "end_match":
                match_id = content
                match_type = match_code_exist(match_id)
                shutil.move(f"{GAME}{match_type}{match_id}.json",f"{GAME}Ended/{match_id}.json")
                with open(f"{GAME}Ended/{match_id}.json","r") as file:
                    data = json.load(file)
                data["Rematch"] = 0
                with open(f"{GAME}Ended/{match_id}.json","w") as file:
                    file.write(json.dumps(data,indent=1,ensure_ascii=False))
            elif command == "rematch":
                match_id = content
                match_type = match_code_exist(match_id)
                shutil.move(f"{GAME}{match_type}{match_id}.json",f"{GAME}Ended/{match_id}.json")
                with open(f"{GAME}Ended/{match_id}.json","r") as file:
                    data = json.load(file)
                data["Rematch"] += 1
                if data["Rematch"] == data["Size"]:
                    create_game(data["Grid"],data["Match Name"],data["Match Code"],"Private")
                    os.remove(f"{GAME}Ended/{match_id}.json")
                else:
                    with open(f"{GAME}Ended/{match_id}.json","w") as file:
                        file.write(json.dumps(data,indent=1,ensure_ascii=False))
            elif command == "delete_match":
                match_id = content
                match_type = match_code_exist(match_id)
                os.remove(f"{GAME}{match_type}{match_id}.json")
            elif command == "fetch_matches":
                page = int(content)
                start = (page-1)*7
                games = os.listdir(f"{GAME}Public/")
                matches = []
                if start >= len(games):
                    conn.send(f"{matches}".encode(self.encode_format))
                end = min(7,len(games)-start)
                for match_id in games[start:start+end]:
                    with open(f"{GAME}Public/{match_id}","r") as file:
                        data = json.load(file)
                    game = {
                        "name":data["Match Name"],
                        "code":data["Match Code"],
                        "grid":data["Grid"],
                        "size":data["Size"],
                        "player":data["Player"]
                    }
                    matches.append(game)
                conn.send(f"{matches}".encode(self.encode_format))
            conn.close()
            
Server(host,port,1).run()

