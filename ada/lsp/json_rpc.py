# Handles JSON-RPC communication
# It should include functions to parse incoming JSON-RPC requests, 
# generate responses, and manage errors.


import json

class JSONRPC:
    @staticmethod
    def parse_request(data):
        try:
            request = json.loads(data)
            # Validate required fields
            if 'jsonrpc' not in request or request['jsonrpc'] != '2.0':
                raise ValueError("Invalid JSON-RPC version")
            if 'method' not in request:
                raise ValueError("Missing 'method' field")
            if 'id' not in request:
                raise ValueError("Missing 'id' field")
            return request
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON data")

    @staticmethod
    def create_response(result, id):
        response = {
            "jsonrpc": "2.0",
            "id": id
        }
        if result is not None:
            response["result"] = result
        return json.dumps(response)

    @staticmethod
    def create_error_response(error, id=None):
        return json.dumps({
            "jsonrpc": "2.0",
            "id": id,
            "error": {
                "code": -32603,
                "message": error
            }
        })