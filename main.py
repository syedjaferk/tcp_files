# Uncomment this to pass the first stage
import socket
import threading



def on_new_client(client_socket):
	request = client_socket.recv(1024)
	request = request.decode("utf-8")
	word = request.split("\r\n")[0].split(" ")[1]
	
	if word == "/":
		status = "HTTP/1.1 200 OK\r\n\r\n"        
		status = status.encode("utf-8")
		client_socket.send(status)
	elif word.startswith("/echo/"):
		message = word.replace("/echo/", "")
		headers = {
		    'Content-Type': 'text/plain',
		    'Content-Length': len(message)
		}
		response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in headers.items()).encode("utf-8")
		status = "HTTP/1.1 200 OK\r\n"        
		status = status.encode("utf-8")
		client_socket.send(status)
		client_socket.send(response_headers_raw)
		client_socket.send("\n".encode("utf-8"))
		client_socket.send(message.encode("utf-8"))
	elif word == "/user-agent":
		user_agent = request.split("\r\n")[2].split(" ")[1]
		status = "HTTP/1.1 200 OK\r\n"        
		status = status.encode("utf-8")
		headers = {
		    'Content-Type': 'text/plain',
		    'Content-Length': len(user_agent)
		}
		response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in headers.items()).encode("utf-8")
		client_socket.send(status)
		client_socket.send(response_headers_raw)
		client_socket.send("\n".encode("utf-8"))
		client_socket.send(user_agent.encode("utf-8"))
	else:
		status = "HTTP/1.1 404 Not Found\r\n\r\n"        
		status = status.encode("utf-8")
		client_socket.send(status)

        

def main():
	
	server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
	while True:
		(client_socket, client_address) = server_socket.accept() # wait for client
		thread = threading.Thread(target=on_new_client, args=(client_socket,))
		thread.start()

if __name__ == "__main__":
    main()
