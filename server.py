import socket
import time
import json
from _thread import *

# https://realpython.com/python-sockets/
# https://www.dunebook.com/creating-a-python-socket-server-with-multiple-clients/

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
    start_new_thread(client_handler, (Client, ))  # TODO: i dont think i need a new thread for each socket
    #                                                   https://medium.com/fantageek/understanding-socket-and-port-in-tcp-2213dc2e9b0c


def client_handler(connection):
    print("Connection number " + str(ThreadCount) + ".")
    while True:
        data = connection.recv(1024).decode('utf-8')
        split_data = data.split(" ", 1)
        dataID = (split_data[0])  # each thing that the client sends will have an ID labeling what its trying to do
        #  and a message accompanying it sometimes
        try:
            message = (split_data[1])
        except IndexError:
            message = ""  # if theres just an ID, set the message to nothing
        if dataID == "LOGIN":
            login(message, connection)
        if dataID == "CREATE":
            createaccount(message, connection)
    connection.close()  # FIXME: make code reachable by letting user disconnect via input


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
    f.write(new_data)  # FIXME: rewriting file every time means users can overwrite each other - create shadow
    #                       versions to give each user, then queue changes in server (or something like that)
    connection.send(bytes("CREATIONSUCCESS", 'utf-8'))
    f.close()


start_server(host, port)
