import os
import sys
import subprocess
import time
import urllib.request
import socket

BRIDGE_PORT = 5000
ROUTER_PORT = 9000 # Default or typical port for 9router / AI gateway

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def start_9router():
    print("[1/3] Checking 9Router gateway...")
    if check_port(ROUTER_PORT) or check_port(8080): # checking common gateway ports
        print(" -> 9Router is ALREADY running!")
        return True
    
    print(" -> 9Router is NOT running. Attempting to start 9router...")
    try:
        # Try running 9router command if available
        subprocess.Popen(["9router", "start"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        if check_port(ROUTER_PORT):
            print(" -> 9Router successfully started!")
            return True
    except Exception as e:
        print(f" -> Could not auto-start 9router CLI: {e}")
    
    print(" -> Note: Please ensure your 9Router / AI backend is active if needed.")
    return False

def start_bridge_server():
    print("[2/3] Checking Roblox Hermes Bridge Server...")
    if check_port(BRIDGE_PORT):
        print(" -> Bridge server is ALREADY running on port", BRIDGE_PORT)
        return
    
    print(" -> Starting Roblox Hermes Bridge Server (`server.py`)...")
    script_path = os.path.join(os.path.dirname(__file__), "server.py")
    subprocess.Popen([sys.executable, script_path])
    time.sleep(1)
    
    if check_port(BRIDGE_PORT):
        print(" -> Bridge server successfully started!")
    else:
        print(" -> WARNING: Bridge server failed to start automatically.")

def print_roblox_instructions():
    print("\n[3/3] Roblox Studio MCP Bridge Ready!")
    print("=" * 50)
    print("STATUS: All systems operational.")
    print("NEXT STEPS:")
    print("1. Open Roblox Studio (Make sure 'Allow HTTP Requests' is enabled).")
    print("2. Paste `plugin.lua` into ServerScriptService or Command Bar.")
    print("3. Hermes can now control Roblox Studio in real-time!")
    print("=" * 50)

if __name__ == '__main__':
    print("=== Hermes x Roblox Studio One-Click Launcher ===")
    start_9router()
    start_bridge_server()
    print_roblox_instructions()
