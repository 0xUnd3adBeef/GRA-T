# GRA-T — Goatesque Remote Administration Tool


> **Usage scope:** GRA-T is mostly a bot i've made for the fun of it. Feel free to tweak it as you want. You are responsible for complying with laws and contracts.
Little note :
> Ive made this bot just for the fun of it, testing my knowledge and exploring with python, it is not meant to be reliable at all.
> It used to be completely undetected by fully updated : Bitdefender, Windows Security, Avast, Avira and kaspersky (All of them which were UNACTIVATED, free versions may be limited)
> Also I thought it'd be a good idea to establish remote code execution via well known platforms (discord, telegram, teams and all platforms that allow such stuff) because you can exploit the "trust" people have towards these;
> Let's say a SOC operator sees some microsoft teams or discord traffic,  it has better chances of not being detected than a domain called `gxqxyu4q6e.ru` (random domain)
>
> Well, you now get the idea

---

## Overview

| Field           | Value                                                                 |
| --------------- | --------------------------------------------------------------------- |
| Category        | Post-exploitation / remote administration over Discord slash commands |
| Modes           | **Vanilla** (core features), **Fat** (core + plugin framework)        |
| OS Support      | Windows (full) / Linux (partial)                                      |
| Control Channel | Discord bot (discord.py + slash commands)                             |
| Author          | @0xUnd3adBeef                                                         |
| Intended Use    | Authorized pentests, red-team labs, research                          |

---

## Key Features

* Shell execution: `cmd`, `powershell`, `bash` (slash commands)
* File ops: upload/download, directory nav (`cd`, `ls`, `find`)
* System intel: system info embed + screenshot, public IP lookup
* Windows-only helpers: enable RDP + admin user creation; UAC elevation attempt; Defender exclusion (admin)
* Process & service tooling: list/kill processes; list services (slash command groups)
* Remote script runner: pull and execute `.bat` / `.ps1` / `.exe` from GitHub (hidden dir, silent)
* TTS (lab/demo utility)&#x20;
* **Plugin framework** (Fat): import/list/info/use/stop/delete/sethook for `.grataddin` plugins (Python/PowerShell/Batch/Bash)&#x20;

---

## Modes & Command Matrix

| Command / Group                                                                                                                                                              | Vanilla | Fat |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----: | :-: |
| `/clean`, `/ping`, `/systeminfo`                                                                                                                                             |    ✅    |  ✅  |
| `/cd`, `/ls`, `/find`                                                                                                                                                        |    ✅    |  ✅  |
| `/run`, `/runcmd`, `/runsh`, `/runpwsh`                                                                                                                                      |    ✅    |  ✅  |
| `/upload`, `/download`                                                                                                                                                       |    ✅    |  ✅  |
| `/ip`, `/tts`                                                                                                                                                                |    ✅    |  ✅  |
| `/uac`, `/exclude`, `/unpersist`                                                                                                                                             |    ✅    |  ✅  |
| `/setup_rdp` (Windows, insta detect)                                                                                                                                                       |    ✅    |  ✅  |
| `/process list`, `/process kill`                                                                                                                                             |    ✅    |  ✅  |
| `/service list`                                                                                                                                                              |    ✅    |  ✅  |
| `/rungit` (GitHub script/EXE runner)                                                                                                                                         |    ✅    |  ✅  |
| **Plugin system**: `/plugin_import`, `/plugin_list`, `/plugin_info`, `/plugin_use`, `/plugin_stop`, `/plugin_stopall`, `/plugin_delete`, `/plugin_sethook`, `/plugin` (help, insta detect) |    ❌    |  ✅  |

Sources: Vanilla/Fat implementations of the same command sets, plus plugin APIs in Fat.

---

## Plugin Framework (`.grataddin`) — Fat Mode

* **Languages:** Python, PowerShell, Batch (cmd), Bash
* **Metadata header (parsed):** `plugin.name`, `plugin.description`, `plugin.lang`, `plugin.ositworkswith`, `plugin.commands`, `plugin.args`
* **Lifecycle:** `import → list/info → use → stop/stopall → delete`
* **Webhooks:** per-user plugin output via `/plugin_sethook` (env `GRA_T_PLUGIN_WEBHOOK`)

All of this is implemented in the Fat build’s plugin manager and command set.&#x20;

---

## Install

### Requirements

* Python 3.10+ 
* Packages used by code: `discord.py`, `requests`, `pyautogui` (screenshots), plus stdlib (`asyncio`, `subprocess`, etc.)

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install discord.py requests pyautogui
```


### Configuration

1. Create a Discord application & bot, enable **Message Content Intent**.
2. Copy the bot token into the script (`BOT_TOKEN`).
3. (Optional) Adjust the channel ID used on ready events.

---

## Run

To run this tool you can run it using python in a command line or pack it into an exe / elf file using pyinstaller.

On first connect the bot syncs slash commands and can post a system info embed with screenshot on request.

---

## Usage (Selected)

> All commands are **slash commands**. Names shown below match handlers in the code.

* **System & Recon**

  * `/systeminfo` – embed with OS, version, arch, privs, public IP + screenshot
  * `/ip` – public IP via web API&#x20;

* **Execution**

  * `/run`, `/runcmd`, `/runsh`, `/runpwsh` – run native shell/programs; output returned (split if large)
  * `/rungit <url> [args]` – download & run `.bat` / `.ps1` / `.exe` from GitHub in a hidden working dir, capture output file(s)

* **Files & Dirs**

  * `/upload`, `/download`, `/cd`, `/ls`, `/find`&#x20;

* **Windows Ops**

  * `/setup_rdp` – enable RDP, create admin user w/ random password, return connection info (Windows-only)&#x20;
  * `/uac` – attempt elevation via ShellExecuteW runas; Linux path reports guidance only&#x20;
  * `/exclude` – add Defender exclusion for current folder (admin required) **for lab use**&#x20;

* **Processes & Services**

  * `/process list` / `/process kill <name|PID>`; `/service list`&#x20;

* **Misc**

  * `/tts`, `/clean`, `/ping`, `/help`, `/leave` (graceful exit)&#x20;

* **Plugins (Fat)**

  * `/plugin_import`, `/plugin_list`, `/plugin_info`, `/plugin_use <name> <args>`, `/plugin_stop`, `/plugin_stopall`, `/plugin_delete`, `/plugin_sethook <url>`, `/plugin` (help)&#x20;

---

## Architecture (High-Level)

* **Core:** Python + `discord.py` slash commands, intents enabled, structured logging
* **Exec:** `subprocess` wrappers for OS shells; large outputs chunked to files for Discord limits
* **Screenshots:** `pyautogui` (PNG)
* **Basic Automatic Persistence (Windows/Linux):** Startup folder copy / `.desktop` autostart (Vanilla); hidden startup copy on Windows (Fat)
* **Plugins (Fat):** on-disk `.grataddin` with JSON metadata cache, PID tracking, per-user webhooks, language-specific launchers&#x20;

---

## Security Notes

* No unsolicited beaconing; everything is operator-driven via Discord slash commands.&#x20;
* Bot permissions are tied to your Discord app/role model; treat tokens as secrets.
* Features that alter system configuration are to be treated with caution.&#x20;

---

## Limitations

* Linux support is partial vs. Windows (RDP, AV exclusion, UAC are Windows-specific).&#x20;
* Discord file size constraints; outputs are chunked when needed.&#x20;


---

## Roadmap

* Plugin signing/verification & safer at-rest storage
* Additional platforms (Teams, Slack)
* VM/sandbox detection
* Cross-platform parity improvements

---

## Contributing

PRs welcome for:

* New `.grataddin` plugins (Fat)
* OS-compatibility improvements
* Documentation & examples

Open issues before large changes.

---

## Legal

Use only with explicit authorization. I am **not** liable for misuse.
Cool kids don't hack when they don't have the authorization
