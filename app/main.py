# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    server_socket = socket.create_server(("localhost", 4221)) #, reuse_port=True)
    connection, address = server_socket.accept() # wait for client
    
    # Read data from a connection
    data = connection.recv(1024)

    # Extract URL path and handle it
    data_str = str(data)
    lines = data_str.split()[1] 
    path = lines.split('/')
    target_path = path.pop()
    
    # Assign content length for the response
    path_size = len(target_path)
    
    # Send back appropriate response
    response = f'HTTP/1.1 404 Not Found\r\n\r\n'
    if path[-1] == "echo" or path[-1] == "":
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {path_size}\r\n\r\n{target_path}'

    connection.send(str.encode(response))
    connection.close()
    
 
if __name__ == "__main__":
    main()