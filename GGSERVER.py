import socket
import random

host = "0.0.0.0"
port = 7777
banner = """
== Guessing Game v1.0 ==
Enter your guess:"""


def generate_random_int(difficulty):
    if difficulty == "easy":
        return random.randint(1, 50)
    elif difficulty == "medium":
        return random.randint(1, 100)
    else:
        return random.randint(1, 500)


def leaderboard_file():
    leaderboard = {}
    try:
        with open("Leaderboard.txt", "r") as file:
            for line in file:
                name, score, difficulty = line.strip().split(",")
                leaderboard[name] = {"score": int(score), "difficulty": difficulty}
    except FileNotFoundError:
        pass
    return leaderboard


# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"server is listening in port {port}")
guessme = 0
conn = None
while True:
    if conn is None:
        print("waiting for connection..")
        conn, addr = s.accept()
        print(f"new client: {addr[0]}")
        conn.sendall(banner.encode())
        conn.sendall(
            b"Choose difficulty level: easy (1-50), medium (1-100), hard (1-500): "
        )
        difficulty = conn.recv(1024).decode().strip().lower()
        conn.sendall(b"Enter your name: ")
        name = conn.recv(1024).decode().strip().lower()
        guessme = generate_random_int(difficulty)
        conn.sendall(banner.encode)
    else:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        print(f"User guess attempt: {guess}")
        if guess == guessme:
            conn.sendall(b"Correct Answer!")
            conn.close()
            conn = None
            continue
        elif guess > guessme:
            conn.sendall(b"Guess Lower!\nenter guess: ")
            continue
        elif guess < guessme:
            conn.sendall(b"Guess Higher!\nenter guess:")
            continue
