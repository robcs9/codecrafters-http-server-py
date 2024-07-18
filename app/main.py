# Uncomment this to pass the first stage
import socket
import threading
import argparse
import os

def handle_response(connection):    
    # Uncomment this to pass the first stage
    #server_socket = socket.create_server(("localhost", 4221)) #, reuse_port=True)
    #connection, address = server_socket.accept() # wait for client

    # Read data from a connection
    data = connection.recv(1024)
    # Extract URL path and handle it
    data_str = bytes.decode(data, "utf-8") #str(data)
    req_fields = data_str.split()
    endpoint = data_str.split()[1]
    user_agent = req_fields[-1].split('\\') # user-agent extraction requires better target logic
    url_path = endpoint.split('/')
    req_type = req_fields[0]

    # Directory argument processing
    parser = argparse.ArgumentParser(description="Process directory argument")
    parser.add_argument('--directory')
    args = parser.parse_args()
    
    # Default response
    response = f'HTTP/1.1 404 Not Found\r\n\r\n'

    if len(url_path) > 1 and url_path[1] == 'echo':
        body = url_path[-1]
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}'
    
    elif len(url_path) > 1 and url_path[1] == 'user-agent':
        body = user_agent[0]
        response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n{body}'
    
    elif len(url_path) > 1 and url_path[1] == 'files':
        filename = url_path[-1]
        
        if req_type == "POST":
            file_text = req_fields[-1]
            print(f'{data_str}')
            #print(os.path.dirname())
            with open(f'{args.directory}/{filename}', 'w') as f:
                #print('im here')
                f.write(file_text)
                #print(f.read())
                response = f'HTTP/1.1 201 Created\r\n\r\n'

            #try:
            #    with open(args.directory, 'x') as f:
            #        f.write(file_text)
            #        print(f.read())
            #    response = f'HTTP/1.1 201 Created\r\n\r\n'
            #except Exception:
            #    print("Failed to create new file")
        else:
            try:
                f = open(f'{args.directory}/{filename}', 'r')
                read_data = f.read()
                f.close()
                response = f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(read_data)}\r\n\r\n{read_data}'
            except Exception:
                print("File not found")
    
    elif len(url_path) == 2 and url_path[1] == '':
        response = f'HTTP/1.1 200 OK\r\n\r\n'

    connection.send(str.encode(response))

# Concurrent connections stage
def handle_client(client_socket):
    handle_response(client_socket)
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
    
    # Concurrent connections
    concurrent_connections()
    
if __name__ == "__main__":
    main()