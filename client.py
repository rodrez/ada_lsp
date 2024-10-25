import socket
import json
from typing import Dict, Any

class JSONRPCClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 8080):
        self.host = host
        self.port = port

    def send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps(request).encode('utf-8'))
            
            # Receive response
            data = b''
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                data += chunk
                if len(chunk) < 1024:
                    break
            
            print(f"Raw response: {data}")  # Debug: Print raw response
            
            if not data:
                return {"error": "Empty response from server"}
            
            try:
                # Decode the response if it's a JSON string
                response_str = data.decode('utf-8')
                if response_str.startswith('"') and response_str.endswith('"'):
                    response_str = json.loads(response_str)
                
                response = json.loads(response_str)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return {"error": f"Invalid JSON response: {data.decode('utf-8', errors='replace')}"}
            
            print(f"Sent request: {json.dumps(request, indent=2)}")
            print(f"Received response: {json.dumps(response, indent=2)}")
            
            return response

def main():
    client = JSONRPCClient()
    
    # Initialize request
    initialize_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    
    client.send_request(initialize_request)
    print("Server initialized.")

    # Completion request
    completion_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "textDocument/completion",
        "params": {
            "textDocument": {"uri": "file:///test.adb"},
            "position": {"line": 0, "character": 3},
            "context": {"triggerKind": 1}
        }
    }
    
    completion_response = client.send_request(completion_request)
    
    # Check if the response is a dictionary
    if isinstance(completion_response, dict):
        if 'result' in completion_response:
            print("\nCompletion items:")
            for item in completion_response['result'].get('items', []):
                print(f"- {item}")
        elif 'error' in completion_response:
            print(f"Error in response: {completion_response['error']}")
        else:
            print("Unexpected response format:", completion_response)
    else:
        print("Received non-dictionary response:", completion_response)

if __name__ == "__main__":
    main()
