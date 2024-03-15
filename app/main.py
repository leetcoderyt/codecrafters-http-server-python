import socket
import threading

BUFFER_SIZE = 1024
ENCODING = "utf-8"

def response_with_content(content):
    return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"

def response(path, user_agent):
    if path[0:5] == "/echo":
        random_string = '/'.join(path.split('/')[2:])
        return response_with_content(random_string)
    elif path[0:11] == "/user-agent":
        return response_with_content(user_agent)
    elif path == "/":
        return "HTTP/1.1 200 OK\r\n\r\n"

    return "HTTP/1.1 404 Not Found\r\n\r\n"

def handle_client(client_socket, address):
    print(f"Connection from {address} has been established.")
    data = client_socket.recv(BUFFER_SIZE)
    request = data.decode(ENCODING)
    print(f"Received from client: {request}")

    request_lines = request.split("\r\n")
    path = request_lines[0].split(" ")[1]

    user_agent = None
    for line in request_lines:
        if line.startswith("User-Agent:"):
            user_agent = line.split(" ")[1]
            break

    client_socket.sendall(response(path, user_agent).encode(ENCODING))
    client_socket.close()

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()

    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
