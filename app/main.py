# Uncomment this to pass the first stage
import socket
import threading
#import socketserver
    

# Concurrent connections stage
def handle_client(client_socket):
    data = client_socket.recv(1024)
    client_socket.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n')
    client_socket.close()
    print('Server has been shutdown')

def concurrent_connections():
    HOST = 'localhost'
    PORT = 4221
    server_socket = socket.create_server((HOST, PORT))
    server_socket.listen()
    print(f'Server is listening on port {PORT}')
    
    try:
        while True:
            conn, addr = server_socket.accept()
            print(f'Connection from {addr} has been established!')
            client_handler = threading.Thread(target=handle_client, args=(conn,))
            client_handler.start()
            #print('Server loop running in thread: ', client_handler.name)
    except KeyboardInterrupt:
        print('Server is shutting down')
    finally:
        server_socket.close()
        print('Server has been shutdown')

    

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    def previous_stages():    
        # Uncomment this to pass the first stage
        server_socket = socket.create_server(("localhost", 4221)) #, reuse_port=True)
        connection, address = server_socket.accept() # wait for client

        # Read data from a connection
        data = connection.recv(1024)
        # Extract URL path and handle it
        data_str = str(data)
        req_fields = data_str.split()
        endpoint = data_str.split()[1]
        user_agent = req_fields[-1].split('\\') # user-agent extraction requires better target logic
        path = endpoint.split('/')
        #status_line = 'HTTP/1.1 404 Not Found'
        #headers = '\r\n'
        #body = '\r\n\r\n'

        # Assign content length for the response
        #path_size = len(body)

        # Send back appropriate response
        # ['', 'echo', 'x'] => 202 'x', ['', ''] => 202, ['', 'y'] => 404
        response = f'HTTP/1.1 404 Not Found\r\n\r\n'
        if len(path) > 1 and path[1] == 'echo':
            body = path[-1]
            response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}'
        elif len(path) > 1 and path[1] == 'user-agent':
            body = user_agent[0]
            response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}'
        elif len(path) == 2 and path[1] == '':
            response = f'HTTP/1.1 200 OK\r\n\r\n'

        #print(body)
        connection.send(str.encode(response))
        connection.close()
    
    # Concurrent connections
    concurrent_connections()
    
 
if __name__ == "__main__":
    main()