import socket


host = "localhost"
port = 7777

while True:
    s = socket.socket()
    s.connect((host, port))

    # received the banner
    data = s.recv(1024)
    # print banner
    print(data.decode().strip())

    difficulty = input("").strip().lower()
    s.sendall(difficulty.encode())

    data = s.recv(1024)
    print(data.decode().strip())

    while True:
        # let get our input from the user
        user_input = input("").strip()

        s.sendall(user_input.encode())
        reply = s.recv(1024).decode().strip()
        if "Correct" in reply:
            print(reply)
            break
        print(reply)
        continue
    s.close()

    again = input("Do you want to play again? Enter (y)/(n): ").strip().lower()
    if again != "y":
        break
