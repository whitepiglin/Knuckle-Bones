import socket
import json
import random
import os

from mechanic import *

GAME = ""

def create_LAN_game(grid,match_name):
    data = {
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
        "Placed": [[-1,-1] for i in range(0,2)],
        "Rematch": 0,
        "Ended": 0
    }
    return data

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

def start_LAN_sever(host,port,grid,match_name):
    data = create_LAN_game(grid,match_name)
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    server.bind((host,port))
    server.listen(1)
    activate = True
    while activate:
        conn, addr = server.accept()
        command = conn.recv(1024).decode()
        print(command)
        content = command.split(":")[1]
        command = command.split(":")[0]
        if command == "get_match":
            conn.send(f"{data}".encode())
        elif command == "update_match":
            section = content.split(',')[0]
            action = content.split(',')[1]
            if "Board" in section:
                temp = content.split(',')[1:]
                action = ""
                for t in temp:
                    action += t
                action = action.replace("(","").replace(")","").split(" ")
                for i in range(0,len(action)):
                    action[i] = int(action[i])
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
                if finish_board(data["Player 1 Board"]) or finish_board(data["Player 2 Board"]):
                    data["Rematch"] = 0
                    data["Ended"] = 1
            elif section == "Placed":
                temp = content.split(',')[1:]
                action = ""
                for t in temp:
                    action += t
                action = action.replace("[","").replace("]","").split(" ")
                data[section][int(action[0])] = [int(action[1]),int(action[1])]
            else:
                data[section] = int(action)
        elif command == "end_match":
            data["Rematch"] = 0
            data["Ended"] = 1
        elif command == "rematch":
            data["Rematch"] += 1
            if data["Rematch"] == data["Size"]:
                data = create_LAN_game(data["Grid"],data["Match Name"])
                data["Rematch"] = data["Size"]
        elif command == "delete_match":
            activate = False
        conn.close()

def get_LAN_match(address):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect(address)
    command = f"get_match:"
    client.send(command.encode())
    respond = client.recv(1024).decode()
    return respond

def update_LAN_match(address,section,action):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect(address)
    command = f"update_match:{section},{action}"
    client.send(command.encode())

def delete_LAN_match(address):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect(address)
    command = f"delete_match:"
    client.send(command.encode())
    respond = client.recv(1024).decode()
    return respond

def end_LAN_match(address):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect(address)
    command = f"end_match:"
    client.send(command.encode())
    respond = client.recv(1024).decode()
    return respond

def LAN_rematch(address):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect(address)
    command = f"rematch:"
    client.send(command.encode())
    respond = client.recv(1024).decode()
    return respond