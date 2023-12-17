import socket
import time
import json
from _thread import *

# https://realpython.com/python-sockets/
# https://www.dunebook.com/creating-a-python-socket-server-with-multiple-clients/

# TODO: create a terminal - act on players (disconnect), the save file (scan through to make sure all names r legit)
# TODO: create a log of every time server runs, who connects, who disconnects, what actions terminal does, timestamps
#   if no server logs found in server's directory, ask if user has set up server properly for play
# TODO: lag sending info for login and create account (esp create account) to avoid spam

host = '127.0.0.1'
port = 65535
ThreadCount = 0  # number of connections


def start_server(host, port):
    s = socket.socket()
    try:
        s.bind((host, port))
    except socket.error as e:
        print(str(e))
    print(f'Your server (IP {host}) is listening (Port {port}).')
    s.listen()
    while True:
        accept_connections(s)


def accept_connections(s):
    Client, address = s.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (Client, ))


def client_handler(connection):
    connection.sendall(b'HANDSHAKE')  # todo: temporary
    connection.setblocking(False)
    while True:
        try:
            data = connection.recv(1024).decode('utf-8')
            split_data = data.split(" ", 1)
            dataID = (split_data[0])  # each thing that the client sends will have an ID labeling what its trying to do
            #  and a message accompanying it sometimes
            try:
                message = (split_data[1])
            except IndexError:
                message = ""  # if theres just an ID, set the message to nothing
        except BlockingIOError:
            # waiting
            data = ""
            dataID = data
            message = dataID
        if dataID == "LOGIN":
            login(message, connection)
        if dataID == "CREATE":
            createaccount(message, connection)
        if dataID == "CLOSE":
            connection.close()


def login(message, connection):
    username = (message.split("USERNAME", 1)[1].split("PASSWORD", 1))[0].strip()
    password = (message.split("USERNAME", 1)[1].split("PASSWORD", 1))[1].strip()
    f = open('savefile.json', 'r')
    data = json.load(f)
    for i in data['userDB']:
        if i['username'] == username:
            if i['password'] == password:
                connection.send(bytes("LOGINSUCCESS", 'utf-8'))
                f.close()
    connection.send(bytes("LOGINFAILURE", 'utf-8'))
    f.close()


def createaccount(message, connection):
    username = (message.split("USERNAME")[1].split("PASSWORD"))[0].strip()
    password = (message.split("USERNAME")[1].split("PASSWORD"))[1].strip()
    admin_status = False
    f = open('savefile.json', 'r')
    data = json.load(f)
    for i in data['userDB']:
        if username.lower() == i['username'].lower():
            connection.send(bytes("CREATIONFAILURE", 'utf-8'))
            f.close()
            return
    # my JSON format is a dictionary with a key 'userDB', its value being a list, and each element in the list
    # is a dictionary of user info. that might be why i was struggling to parse and write to it.
    new_user_info = {"username": username,
                     "password": password,
                     "admin": admin_status}
    data['userDB'].append(new_user_info)
    new_data = json.dumps(data, indent=4)
    f.close()
    f = open('savefile.json', 'w')  # reopens the file to overwrite
    f.write(new_data)  # optimize: rewriting file every time means users can overwrite each other - create shadow
    #                       versions to give each user, then queue changes in server (or something like that)
    #                       also when closing server upload file online so that multiple servers can run at once
    #                       and itll still be the same game
    connection.send(bytes("CREATIONSUCCESS", 'utf-8'))
    f.close()


start_server(host, port)
