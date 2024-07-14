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
    req_fields = data_str.split()
    endpoint = data_str.split()[1]
    user_agent = req_fields[4]
    path = endpoint.split('/')
    status_line = 'HTTP/1.1 404 Not Found'
    headers = '\r\n'
    body = '\r\n\r\n'
    
    # Assign content length for the response
    #path_size = len(body)
    
    # Send back appropriate response
    # ['', 'echo', 'x'] => 202 'x', ['', ''] => 202, ['', 'y'] => 404
    response = f'HTTP/1.1 404 Not Found\r\n\r\n'
    if len(path) > 1 and path[1] == 'echo':
        body = path[-1]
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}'
    if len(path) > 1 and path[1] == 'user-agent':
        body = user_agent
        print(body)
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}'
    if len(path) == 2 and path[1] == '':
        response = f'HTTP/1.1 200 OK\r\n\r\n'

    connection.send(str.encode(response))
    connection.close()
    
 
if __name__ == "__main__":
    main()