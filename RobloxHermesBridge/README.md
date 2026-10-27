# Roblox Studio x Hermes MCP Bridge 🚀

Connect **Hermes Agent** and **9Router AI Gateway** directly to **Roblox Studio** using the **Model Context Protocol (MCP)** for real-time AI vibe coding and game automation.

---

## ⚡ Quick Start (One Command Setup)

Clone the repository and run the automated installer:

```bash
git clone https://github.com/liptz341/RobloxHermesBridge.git
cd RobloxHermesBridge
python setup.py
```

### What `setup.py` does automatically:
1. **9Router Integration**: Optionally prompts for your 9Router AI Gateway endpoint and API key, configuring Hermes custom provider settings.
2. **Hermes Agent Check & Install**: Detects if Hermes is installed, or automatically installs it for you.
3. **Roblox Studio MCP Binding**: Automatically discovers your local Roblox Studio MCP server (`mcp.bat`), registers it in Hermes, and auto-enables all 28 powerful tools.

---

## 🛠️ Available MCP Tools (Powered by Roblox Studio)

Once set up, Hermes can interact directly with your open Roblox Studio session:
- **`execute_luau`**: Run Luau code in Edit, Client, or Server data models.
- **`script_read` & `multi_edit`**: Read and modify scripts using dot-notation paths.
- **`script_search` & `script_grep`**: Search across all game scripts.
- **`generate_procedural_model` & `generate_mesh`**: AI-driven 3D asset generation.
- **`start_stop_play`**: Control playtesting state.
- **`screen_capture`**: Inspect the Roblox Studio viewport.

---

## 📁 Repository Structure
- `setup.py` — Fully automated interactive setup script.
- `server.py` & `plugin.lua` — HTTP bridge fallback server.
- `client_cli.py` — CLI command dispatch helper.
- `README.md` — Documentation.

---

## 📜 License
MIT License. Built for the Roblox & AI community.
