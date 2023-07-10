import socket
from hashlib import sha256
import time
import pygame
# TODO render all fonts with the font_name.render(text, True, (0, 0, 0)) at the beginning
# stuff for me
pygame.init()
red = (255, 0, 0)
black = (0, 0, 0)
gray = (127, 127, 127)
white = (255, 255, 255)
monospaced_font = pygame.font.Font("Courier Std Medium.otf", 36)
not_ugly_font = pygame.font.Font("YsabeauInfant.ttf", 30)
button_text_font = pygame.font.Font("YsabeauInfant.ttf", 40)
pygame.font.get_fonts()

PORT = 65535  # The port used by the server


# https://www.dunebook.com/creating-a-python-socket-server-with-multiple-clients/

# TODO: queue an action, have action finish at the end of the loop
#   have a timeout system where if a response is not given in 10 seconds just retry
# TODO: write in transformations based on server input on where u should be, then flip screen at the very end
# TODO: currently all calls are blocking, when game starts use s.setblocking(False) to set them to non-blocking
#   use a try-except and catch BlockingIOError bc data transmission isnt instant
#   (can also use time to determine ping)
# TODO: medieval styled game maybe
# port forwarding, static IPs

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# start pygame game
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("client.exe")

# connect to the server
running = True
user_text = ""


def login():
    username = ""
    password = ""
    username_active = False
    password_active = False
    while running:
        screen.fill(white)
        username_box = pygame.Rect(25, 125, 350, 50)
        if username_active:
            pygame.draw.rect(screen, gray, username_box)
        pygame.draw.rect(screen, black, username_box, 2)
        username_txt = not_ugly_font.render("Username:", True, (0, 0, 0))
        screen.blit(username_txt, (username_box.x, username_box.y - 40))
        password_box = pygame.Rect(25, 225, 350, 50)
        if password_active:
            pygame.draw.rect(screen, gray, password_box)
        pygame.draw.rect(screen, black, password_box, 2)
        password_txt = not_ugly_font.render("Password:", True, (0, 0, 0))
        screen.blit(password_txt, (password_box.x, password_box.y - 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_box.collidepoint(event.pos):
                    username_active = True
                    password_active = False
                elif password_box.collidepoint(event.pos):
                    username_active = False
                    password_active = True
                else:
                    username_active = False
                    password_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if username_active:
                        username = username[:-1]
                    elif password_active:
                        password = password[:-1]
                elif event.key == pygame.K_RETURN:
                    s.sendall(bytes("LOGIN USERNAME " + username + " PASSWORD "
                                    + sha256(password.encode('utf-8')).hexdigest(), "utf-8"))
                    data = s.recv(1024)
                    if data == bytes("LOGINSUCCESS", 'utf-8'):
                        return "success"
                    if data == bytes("LOGINFAILURE", 'utf-8'):
                        return
                elif event.key == pygame.K_TAB:
                    if username_active or password_active:
                        username_active = not username_active
                        password_active = not password_active
                    else:
                        username_active = True
                else:
                    if username_active:
                        if len(username) < 15:  # TODO: only allow certain characters to be inputted into username
                            username += event.unicode
                        else:
                            pygame.draw.rect(screen, red, username_box, 2)
                    elif password_active:
                        password += event.unicode
                        #   if text is bigger than box, shift it to the left the length of one character, if that
                        # goes outside of the box / margin then delete it
        username_display = monospaced_font.render(username, True, (0, 0, 0))
        screen.blit(username_display, (username_box.x + 5, username_box.y + 9))
        password_display = monospaced_font.render("*"*len(password[:15]), True, (0, 0, 0))  # optimize it looks ugly
        screen.blit(password_display, (password_box.x + 5, password_box.y + 9))
        pygame.display.flip()


def createaccount():
    username = ""
    password = ""
    username_active = False
    password_active = False
    while running:
        screen.fill(white)
        username_box = pygame.Rect(25, 125, 350, 50)
        if username_active:
            pygame.draw.rect(screen, gray, username_box)
        pygame.draw.rect(screen, black, username_box, 2)
        username_txt = not_ugly_font.render("Create username:", True, (0, 0, 0))
        screen.blit(username_txt, (username_box.x, username_box.y - 40))

        password_box = pygame.Rect(25, 225, 350, 50)
        if password_active:
            pygame.draw.rect(screen, gray, password_box)
        pygame.draw.rect(screen, black, password_box, 2)
        password_txt = not_ugly_font.render("Set password:", True, (0, 0, 0))
        screen.blit(password_txt, (password_box.x, password_box.y - 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_box.collidepoint(event.pos):
                    username_active = True
                    password_active = False
                elif password_box.collidepoint(event.pos):
                    username_active = False
                    password_active = True
                else:
                    username_active = False
                    password_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if username_active:
                        username = username[:-1]
                    elif password_active:
                        password = password[:-1]
                elif event.key == pygame.K_RETURN:
                    s.sendall(bytes("CREATE USERNAME " + username + " PASSWORD "
                                    + sha256(password.encode('utf-8')).hexdigest(), "utf-8"))
                    data = s.recv(1024)
                    if data == bytes("CREATIONSUCCESS", 'utf-8'):
                        return "success"
                    if data == bytes("CREATIONFAILURE", 'utf-8'):
                        return
                elif event.key == pygame.K_TAB:
                    if username_active or password_active:
                        username_active = not username_active
                        password_active = not password_active
                    else:
                        username_active = True
                else:
                    if username_active:
                        username += event.unicode   # TODO: set limits for usernames (size = 15 and characters)
                    elif password_active:
                        password += event.unicode
                        #   if text is bigger than box, shift it to the left the length of one character, if that
                        # goes outside of the box / margin then delete it
        username_display = monospaced_font.render(username, True, (0, 0, 0))
        screen.blit(username_display, (username_box.x + 5, username_box.y + 9))
        if len(password) > 15:
            password_display = monospaced_font.render(password[len(password)-15:], True, (0, 0, 0))
        else:
            password_display = monospaced_font.render(password, True, (0, 0, 0))
        screen.blit(password_display, (password_box.x + 5, password_box.y + 9))
        pygame.display.flip()


def accountsys():
    while running:
        screen.fill(white)
        login_button = pygame.Rect(screen.get_width() / 2 - 100, screen.get_height() / 2 - 90, 200, 80)
        if login_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, gray, login_button)
        pygame.draw.rect(screen, black, login_button, 2)
        login_txt = button_text_font.render("LOGIN", True, (0, 0, 0))
        screen.blit(login_txt, (login_button.x + 40, login_button.y + 10))

        create_button = pygame.Rect(screen.get_width() / 2 - 100, screen.get_height() / 2 + 40, 200, 80)
        if create_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, gray, create_button)
        pygame.draw.rect(screen, black, create_button, 2)
        create_txt = button_text_font.render("CREATE", True, (0, 0, 0))
        screen.blit(create_txt, (create_button.x + 25, create_button.y + 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.collidepoint(event.pos):
                    if login() == "success":
                        print("Success!")
                    else:
                        print("incorrect username or password")
                        # TODO: fail
                if create_button.collidepoint(event.pos):
                    if createaccount() == "success":
                        print("Success!")
                        pass  # todo "final" line
                    else:
                        print("unable to make account. retry with a different username or password.")
                        pass  # TODO: fail
        pygame.display.flip()


def attempt_connection():
    loading = True
    if user_text == "":  # makes host the user input (unless blank, then its local)
        HOST = "127.0.0.1"
    else:
        HOST = user_text
    try:  # TODO: instead of writing all of this code here, write it all when the function is called
        #       try attempt_connection except socket.gaierror except connectionrefusederror
        s.connect((HOST, PORT))
    except socket.gaierror:
        incorrect_server_ip = True
        loading = False
        return
    except ConnectionRefusedError:
        server_offline = True
        loading = False
        # maybe have a variable like "error message active" and then have the variable on for 5 seconds, and display
        # while active
        return
    except TimeoutError:
        error_server_offline = True
        error_loading = False
        return
    except OSError as exc:
        if exc.errno == 10056:
            loading = False
            accountsys()
    except:
        loading = False
    accountsys()  # TODO: move this out of the try
    return


while running:
    screen.fill(white)         # (screen dimension / 2) - (box dimension / 2) is in the middle
    startup_txt = not_ugly_font.render("Enter server IP:", True, (0, 0, 0))
    screen.blit(startup_txt, (105, 180))
    server_ip_box = pygame.Rect(25, 225, 350, 50)  # hardcoding values rn, in the game the box will be resizeable
    server_ip_button_display = pygame.draw.rect(screen, black, server_ip_box, 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()
        # does text input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_0 or event.key == pygame.K_1 or event.key == pygame.K_2 or \
                    event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or \
                    event.key == pygame.K_6 or event.key == pygame.K_7 or event.key == pygame.K_8 or \
                    event.key == pygame.K_9 or event.key == pygame.K_PERIOD:  # makes sure user is typing in an IP
                if len(user_text) < 15:  # makes sure text will fit in box, blinks red otherwise
                    user_text += event.unicode
                else:
                    pygame.draw.rect(screen, red, server_ip_box, 2)
            elif event.key == pygame.K_RETURN:
                attempt_connection()
            else:  # wrong type of character
                pygame.draw.rect(screen, red, server_ip_box, 2)

        # display the text in the box
        IP_display = monospaced_font.render(user_text, True, (0, 0, 0))
        # start at 175 (middle), decrease with every character down to 10 (edge)
        screen.blit(IP_display, (server_ip_box.x + 175-(len(user_text)*11), server_ip_box.y + 12))
        pygame.display.flip()

# TODO: fix all the weirdness with the run variable, just make everything run under one condition
