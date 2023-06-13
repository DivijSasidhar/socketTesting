import socket
from hashlib import sha256

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65535  # The port used by the server
# TODO: queue an action, have action finish at the end of the loop
#   have a timeout system where if a response is not given in 10 seconds just retry
# https://www.dunebook.com/creating-a-python-socket-server-with-multiple-clients/
lc = ""


def login():  # FIXME: universalize where the loop goes.
    # FIXME: it should be client-side, probably in the main code so you can switch from create to login, vice-versa
    while True:
        username = input("Username: ")
        password = input("Password: ")
        s.sendall(bytes("LOGIN "
                        "USERNAME " + username + " PASSWORD " + sha256(password.encode('utf-8')).hexdigest(), "utf-8"))
        while True:
            data = s.recv(1024)
            if data == bytes("LOGINSUCCESS", 'utf-8'):
                return "success"
            if data == bytes("LOGINFAILURE", 'utf-8'):
                print("Incorrect username or password.")
                print(" ")
                return


def createaccount():
    while True:
        username = input("Select username: ")
        password = input("Create password: ")
        s.sendall(bytes("CREATE "
                        "USERNAME " + username + " PASSWORD " + sha256(password.encode('utf-8')).hexdigest(), "utf-8"))
        while True:
            data = s.recv(1024)
            if data == bytes("CREATIONSUCCESS", 'utf-8'):
                return "success"
            if data == bytes("CREATIONFAILURE", 'utf-8'):
                print("Username taken.")
                print("")
                return


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while not(lc == "L" or lc == "l" or lc == "C" or lc == "c"):
        print("[L]ogin or [C]reate an account")
        lc = input()
        if lc == "L" or lc == "l":
            while login() != "success":
                pass
        elif lc == "C" or lc == "c":
            while createaccount() != "success":
                pass
        else:
            print("Invalid input.")

    print("Welcome to the server.")
