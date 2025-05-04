import socket
import os

host = 'IP'
port = 8088

def create_match(grid,match_name,match_code,match_type):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect((host,port))
    command = f"create_game:{grid},{match_name},{match_code},{match_type}"
    client.send(command.encode())
    respond = client.recv(1024).decode()
    if respond == "Error Code 1550: Match already exist":
        respond = None
    return respond

def get_match(id):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect((host,port))
    command = f"get_match:{id}"
    client.send(command.encode())
    respond = client.recv(1024).decode()
    if respond == "Error Code 1402: Match not exist":
        respond = "None"
    elif respond == "Error Code 1002: Match full":
        respond = "Full"
    elif respond == "Error Code 202: Match ended":
        respond = "Ended"
    return respond

def update_match(id,section,action):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect((host,port))
    command = f"update_match:{id},{section},{action}"
    client.send(command.encode())

def delete_match(id):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect((host,port))
    command = f"delete_match:{id}"
    client.send(command.encode())
    respond = client.recv(1024).decode()
    return respond

def end_match(id):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect((host,port))
    command = f"end_match:{id}"
    client.send(command.encode())
    respond = client.recv(1024).decode()
    return respond

def fetch_matches(page):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect((host,port))
    command = f"fetch_matches:{page}"
    client.send(command.encode())
    respond = client.recv(1024).decode()
    return respond

def get_ended_match(id):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect((host,port))
    command = f"get_ended_match:{id}"
    client.send(command.encode())
    respond = client.recv(1024).decode()
    if respond == "Error Code 201: Match deleted":
        respond = "None"
    return respond

def rematch(id):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    client.connect((host,port))
    command = f"rematch:{id}"
    client.send(command.encode())
    respond = client.recv(1024).decode()
    return respond