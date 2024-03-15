import socket

BUFFER_SIZE = 1024
ENCODING = "utf-8"


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established.")

    data = client_socket.recv(BUFFER_SIZE)
    message = data.decode(ENCODING)
    print(f"Received from client: {message}")

    path = message.split("\r\n")[0].split(' ')[1]

    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
        client_socket.sendall(response.encode(ENCODING))
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        client_socket.sendall(response.encode(ENCODING))

    client_socket.close()


if __name__ == "__main__":
    main()
