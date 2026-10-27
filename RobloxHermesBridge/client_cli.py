import sys
import urllib.request
import json

SERVER_URL = "http://localhost:5000"

def send_command(action, **kwargs):
    payload = {"action": action, **kwargs}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(SERVER_URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            print(f"[Sent to Roblox] Success: {res}")
    except Exception as e:
        print(f"[Error] Could not connect to Roblox Bridge server at {SERVER_URL}: {e}")
        print("Make sure server.py is running and Roblox Studio is polling!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 client_cli.py <action> [args]")
        print("Actions: print, create_part, run_code")
        sys.exit(1)
    
    action = sys.argv[1]
    if action == 'print':
        msg = sys.argv[2] if len(sys.argv) > 2 else "Hello from Hermes!"
        send_command('print', message=msg)
    elif action == 'create_part':
        name = sys.argv[2] if len(sys.argv) > 2 else "HermesPart"
        color = sys.argv[3] if len(sys.argv) > 3 else "Bright red"
        send_command('create_part', name=name, color=color, posY=10)
    elif action == 'run_code':
        code = sys.argv[2] if len(sys.argv) > 2 else "print('Hello World')"
        send_command('run_code', code=code)
    else:
        print(f"Unknown action: {action}")
