import socket
import random

host = "0.0.0.0"
port = 7777
banner = """
== Guessing Game v1.0 ==
Enter your guess: """


def generate_random_int(difficulty):
    if difficulty == "easy":
        return random.randint(1, 50)
    elif difficulty == "medium":
        return random.randint(1, 100)
    elif difficulty == "hard":
        return random.randint(1, 500)
    else:
        raise ValueError("Invalid difficulty level")


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


def savefile(leaderboard):
    with open("leaderboard.txt", "w") as file:
        for name, data in leaderboard.items():
            file.write(f"{name}, {data['score']}, {data['difficulty']}\n")


# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"server is listening in port {port}")
guessme = 0
conn = None

leaderboard = leaderboard_file()
while True:
    if conn is None:
        print("waiting for connection..")
        conn, addr = s.accept()
        print(f"new client: {addr[0]}")
        conn.sendall(b"Enter your name: ")
        name = conn.recv(1024).decode().strip().lower()
        conn.sendall(
            b"Choose difficulty level: easy (1-50), medium (1-100), hard (1-500): "
        )
        difficulty = conn.recv(1024).decode().strip().lower()
        userdata = leaderboard.get(name, {"score": 0, "difficulty": difficulty})
        score = userdata["score"]
        difficulty = userdata["difficulty"]
        guessme = generate_random_int(difficulty)
        conn.sendall(banner.encode())
    else:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        print(f"User guess attempt: {guess}")
        if guess == guessme:
            leaderboard[name] = {
                "score": leaderboard.get(name, {"score": 0})["score"] + 1,
                "difficulty": difficulty,
            }
            savefile(leaderboard)
            score = f"Correct Answer! {name} score: {leaderboard[name]['score']}\n"
            conn.sendall(score.encode())
            conn.close()
            conn = None
            continue
        elif guess > guessme:
            conn.sendall(b"Guess Lower!\nenter guess: ")
            continue
        elif guess < guessme:
            conn.sendall(b"Guess Higher!\nenter guess:")
            continue
