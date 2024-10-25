# This will be the main entry point for running the server. 
# It will initialize the necessary components, set up the socket or communication channel, and start listening for requests.
# It will use json_rpc.py to handle incoming and outgoing JSON messages, 
# while routing requests to specific handlers in request_handler.py.

import socket
from ada.lsp.json_rpc import JSONRPC
from ada.lsp.completion import CompletionEngine
import json



class AdaLSPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.completion_engine = CompletionEngine()
        self.is_initialized = False
        self.is_shutting_down = False
        self.json_rpc = JSONRPC()  # Create an instance of JSONRPC
    
    def start(self):
        """Start the server and listen for incoming connections."""
        self.server_socket.bind((self.host, self.port))

        # Listen for incoming connections
        self.server_socket.listen(1)

        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")

            with client_socket:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    self.handle_request(data, client_socket)
        
    def handle_request(self, data, client_socket):
        """Handle the incoming request."""
        try:
            request = self.json_rpc.parse_request(data)
            method = request['method']
            params = request.get('params', {})
            id = request['id']

            if method == 'initialize':
                response = self.initialize(params)
            elif method == 'shutdown':
                response = self.shutdown()
            elif method == 'exit':
                self.exit()
                return
            elif not self.is_initialized:
                response = self.json_rpc.create_error_response("Server not initialized", id)
            elif self.is_shutting_down:
                response = self.json_rpc.create_error_response("Server is shutting down", id)
            elif method == 'textDocument/completion':
                # Handle completion request
                completions = self.completion_engine.complete(params)
                response = self.json_rpc.create_response({"items": completions}, id)
            else:
                # Route other requests to the request handler
                response = self.json_rpc.create_error_response(f"The method {method} does not exist.", id)
            
            # Convert the response dictionary to a JSON string before encoding
            response_json = json.dumps(response)
            client_socket.sendall(response_json.encode('utf-8'))

        except ValueError as e:
            error_response = self.json_rpc.create_error_response(str(e))
            error_response_json = json.dumps(error_response)
            client_socket.sendall(error_response_json.encode('utf-8'))

    def complete(self, params):
        """Handle the textDocument/completion request."""
        # Use the CompletionEngine instance to handle completions
        return self.completion_engine.complete(params)

    def initialize(self, params):
        """Handle the initialize request."""
        if self.is_initialized:
            return {"error": "Server is already initialized"}
        
        self.is_initialized = True
        return {
            "capabilities": {
                "completionProvider": {
                    "triggerCharacters": ["."]
                }
            }
        }

    def shutdown(self):
        """Handle the shutdown request."""
        if self.is_shutting_down:
            return {"error": "Server is already shutting down"}
        
        self.is_shutting_down = True
        return None

    def exit(self):
        """Handle the exit notification."""
        if self.is_shutting_down:
            # Graceful shutdown
            self.server_socket.close()
            exit(0)
        else:
            # Forceful shutdown
            exit(1)

    def close(self):
        """Close the server socket."""
        if hasattr(self, 'server_socket'):
            self.server_socket.close()



if __name__ == "__main__":
    server = AdaLSPServer()
    server.start()
