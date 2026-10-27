import os
import sys
import subprocess
import urllib.request
import platform

def print_banner():
    print("="*60)
    print("       ROBLOX HERMES MCP - ONE COMMAND SETUP")
    print("="*60)

def run_cmd(cmd):
    print(f"[RUN] {cmd}")
    return subprocess.run(cmd, shell=True)

def check_hermes():
    try:
        subprocess.run(["hermes", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_hermes():
    print("[*] Installing Hermes Agent...")
    if platform.system() == "Windows":
        cmd = "powershell -Command \"iwr -useb https://hermes-agent.nousresearch.com/install.ps1 | iex\""
    else:
        cmd = "curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash"
    run_cmd(cmd)

def main():
    print_banner()

    # 1. 9Router Setup
    use_9router = input("Use 9Router AI Gateway? (y/N): ").strip().lower() == 'y'
    base_url = "http://localhost:20128/v1"
    api_key = "dummy"

    if use_9router:
        base_url = input(f"Enter 9Router endpoint [default: {base_url}]: ").strip() or base_url
        api_key = input("Enter 9Router API key: ").strip() or "sk-dummy"
        
        # Save to .env or config
        env_path = os.path.expanduser("~/.hermes/.env")
        os.makedirs(os.path.dirname(env_path), exist_ok=True)
        with open(env_path, "a") as f:
            f.write(f"\n# 9Router\nCUSTOM_API_KEY={api_key}\n")
        print("[+] 9Router configured!")

    # 2. Hermes Check & Install
    if not check_hermes():
        install_hermes()
    else:
        print("[+] Hermes Agent is already installed.")

    # 3. Configure Hermes Provider
    if use_9router:
        run_cmd("hermes config set model.provider custom")
        run_cmd(f"hermes config set model.base_url {base_url}")
        run_cmd("hermes config set model.default KreinCombo")

    # 4. Roblox Studio MCP Auto-Connect
    if platform.system() == "Windows":
        local_app_data = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
        mcp_bat = os.path.join(local_app_data, "Roblox", "mcp.bat")
        
        if os.path.exists(mcp_bat):
            print("[*] Connecting Roblox Studio MCP server...")
            add_cmd = f'echo Y | hermes mcp add Roblox_Studio --command cmd.exe --args /c "{mcp_bat}"'
            run_cmd(add_cmd)
        else:
            print("[!] Roblox Studio mcp.bat not found. Make sure Roblox Studio is installed.")
    else:
        print("[!] Non-Windows platform detected. Configure Roblox Studio MCP manually.")

    print("\n" + "="*60)
    print("SETUP COMPLETE! Run 'hermes' to start.")
    print("="*60)

if __name__ == "__main__":
    main()
