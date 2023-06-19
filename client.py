import socket
from hashlib import sha256
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65535  # The port used by the server
# https://www.dunebook.com/creating-a-python-socket-server-with-multiple-clients/
lc = ""

# TODO: queue an action, have action finish at the end of the loop
#   have a timeout system where if a response is not given in 10 seconds just retry

# TODO: remake like the entire thing in pygame lol


def login():
    username = input("Username: ")
    password = input("Password: ")
    s.sendall(bytes("LOGIN "
                    "USERNAME " + username + " PASSWORD " + sha256(password.encode('utf-8')).hexdigest(), "utf-8"))
    while True:  # FIXME: set this to timeout after a certain amount of time
        data = s.recv(1024)
        if data == bytes("LOGINSUCCESS", 'utf-8'):
            return "success"
        if data == bytes("LOGINFAILURE", 'utf-8'):
            return


def createaccount():
    username = input("Select username: ")
    password = input("Create password: ")
    s.sendall(bytes("CREATE "
                    "USERNAME " + username + " PASSWORD " + sha256(password.encode('utf-8')).hexdigest(), "utf-8"))
    while True:  # FIXME: set this to timeout after a certain amount of time
        data = s.recv(1024)
        if data == bytes("CREATIONSUCCESS", 'utf-8'):
            return "success"
        if data == bytes("CREATIONFAILURE", 'utf-8'):
            return


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    HOST = input("Enter server IP address (local for same IP as connection): ")
    if HOST == "local":
        HOST = "127.0.0.1"
    try:
        s.connect((HOST, PORT))
    except socket.gaierror:
        print("Failed to connect.")
        time.sleep(5)
        exit()
    except ConnectionRefusedError:
        print("Server offline.")
        time.sleep(5)
        exit()
    while not(lc == "L" or lc == "l" or lc == "C" or lc == "c"):
        print("[L]ogin or [C]reate an account")
        lc = input()
        if lc == "L" or lc == "l":
            if login() != "success":
                print("Incorrect username or password.", end="\n\n")
                lc = ""
        elif lc == "C" or lc == "c":
            if createaccount() != "success":
                print("Username taken.", end="\n\n")
                lc = ""
        else:
            print("Invalid input.", lc, end="\n\n\n")

    print("Welcome to the server.")
    time.sleep(5)
