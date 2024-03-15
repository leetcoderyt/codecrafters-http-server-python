import socket

BUFFER_SIZE = 1024
ENCODING = "utf-8"


def response(path):
    if path[0:5] == "/echo":
        random_string = '/'.join(path.split('/')[2:])
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_string)}\r\n\r\n{random_string}"
    elif path == "/":
        return "HTTP/1.1 200 OK\r\n\r\n"

    return "HTTP/1.1 404 Not Found\r\n\r\n"

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established.")

    data = client_socket.recv(BUFFER_SIZE)
    message = data.decode(ENCODING)
    print(f"Received from client: {message}")

    path = message.split("\r\n")[0].split(' ')[1]
    client_socket.sendall(response(path).encode(ENCODING))
    client_socket.close()


if __name__ == "__main__":
    main()
