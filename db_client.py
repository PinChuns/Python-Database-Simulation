import socket

END_OF_TRANSMISSION = chr(4)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 8888))
    try:
        while True:
            command = input("SQL:> ")
            if command.strip().lower() in ("exit", "quit"):
                break
            sock.sendall((command + "\n").encode("utf-8"))
            buffer = ""
            while END_OF_TRANSMISSION not in buffer:
                data = sock.recv(1024)
                if not data:
                    raise IOError("Server disconnected (end-of-stream)")
                buffer += data.decode("utf-8")
            response = buffer.split(END_OF_TRANSMISSION)[0]
            print(response.strip())
    finally:
        sock.close()


if __name__ == "__main__":
    main()
